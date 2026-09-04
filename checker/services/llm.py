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

PROMPT_TEMPLATE = """Analyze this message for scam/phishing red flags common in India.

Message: {message}

{category_hint}

Return ONLY valid JSON, no other text, in this exact shape:
{{"explanation": "2-3 sentence plain-language explanation of why this is or isn't risky", "recommended_action": "one sentence telling the user what to do next"}}"""


def get_llm_explanation(
    text: str,
    matched_category: str | None = None,
    timeout: int = 6
) -> dict:

    category_hint = (
        f"It matches a known '{matched_category}' scam pattern in our database."
        if matched_category
        else ""
    )

    prompt = PROMPT_TEMPLATE.format(
        message=text,
        category_hint=category_hint
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