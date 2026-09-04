import json
import logging
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

logger = logging.getLogger(__name__)

client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)

PROMPT_TEMPLATE = """You are a fraud-analysis assistant reviewing a message already scored by a rule-based and machine-learning detection system used in India. The system has already determined the risk level below — your job is to explain WHY, grounded strictly in the evidence provided. Do not invent red flags that aren't listed. Do not independently re-judge the message or contradict the system's risk level.

Message: {message}

System-determined risk level: {risk_level}
Overall risk score: {score}/100

Evidence found by the detection system:
{evidence_block}

Machine-learning spam classifier verdict: {ml_prediction} ({ml_confidence}% confidence)
{pattern_block}

How to write the explanation, based on risk level:
- HIGH: Point to the specific evidence signals that justify treating this as dangerous, so the user understands exactly what to distrust.
- MEDIUM: Note there are some concerning signals but nothing conclusive — explain what raised suspicion without being alarmist.
- LOW: Explain that little or no suspicious evidence was found. Say the message doesn't show known red flags, rather than declaring it "safe" or "genuine" outright.
- Never claim a HIGH-risk message is safe, and never claim a LOW-risk message is dangerous.

Return ONLY valid JSON, no other text, in this exact shape:
{{"explanation": "2-3 sentence plain-language explanation grounded in the evidence above, matching the {risk_level} risk level", "recommended_action": "one practical sentence telling the user what to do next, appropriate for {risk_level} risk"}}"""


def _format_evidence(evidence: list[str]) -> str:
    if not evidence:
        return "- No specific red-flag signals were detected in this message."
    return "\n".join(f"- {item}" for item in evidence)


def get_llm_explanation(
    text: str,
    risk_level: str,
    score: int,
    evidence: list[str] | None = None,
    ml_prediction: str | None = None,
    ml_confidence: float | None = None,
    matched_category: str | None = None,
    timeout: int = 6,
) -> dict:

    evidence_block = _format_evidence(evidence or [])

    pattern_block = (
        f"Matched known scam pattern category: {matched_category}"
        if matched_category
        else "No match against known scam pattern database."
    )

    prompt = PROMPT_TEMPLATE.format(
        message=text,
        risk_level=risk_level,
        score=score,
        evidence_block=evidence_block,
        ml_prediction=ml_prediction or "Unknown",
        ml_confidence=ml_confidence if ml_confidence is not None else "N/A",
        pattern_block=pattern_block,
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        content = response.text.strip()

        if content.startswith("```"):
            content = content.strip("`")
            if content.startswith("json"):
                content = content[4:]

        parsed = json.loads(content.strip())

        return {
            "explanation": parsed.get("explanation", "").strip(),
            "recommended_action": (
                parsed.get("recommended_action", "").strip()
                or None
            ),
        }

    except Exception:
        logger.exception(
            "LLM explanation call failed — using deterministic fallback"
        )

        return {
            "explanation": (
                "Automated explanation is unavailable right now — "
                "this assessment is based on rule-based and "
                "pattern-matching signals only."
            ),
            "recommended_action": None,
        }