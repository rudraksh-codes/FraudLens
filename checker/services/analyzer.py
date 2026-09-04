from .llm import get_llm_explanation
from .matching import match_campaign, normalize
from .ml_model import spam_ham_detector
from .rules import check_rules
from .scoring import calculate_score, get_recommended_action, get_risk_level


def _flatten_evidence(rule_evidence: list[dict]) -> list[str]:
    """rules.py returns structured evidence (type/message/matches) for
    future dashboard breakdowns. checker.html currently expects a flat
    list of strings — this is the one place that boundary is crossed,
    so the template doesn't need to change."""
    flat = []
    for item in rule_evidence:
        if item["type"] == "url":
            flat.extend(item.get("url_signals", []))
            if item["matches"]:
                flat.append(f"{item['message']}: {', '.join(item['matches'])}")
        else:
            flat.append(f"{item['message']}: {', '.join(item['matches'])}")
    return flat


def analyze_text(text: str) -> dict:
    if not text or not text.strip():
        raise ValueError("Text cannot be empty.")

    text = text.strip()[:2000]

    rule_result = check_rules(text)
    ml_result = spam_ham_detector(text)

    normalized = normalize(text)
    matched_pattern, match_score = match_campaign(normalized)
    pattern_score = match_score if matched_pattern else 0

    score = calculate_score(rule_result["score"], ml_result, pattern_score)
    risk_level = get_risk_level(score)

    llm_result = get_llm_explanation(
        text,
        matched_category=matched_pattern.get_category_display() if matched_pattern else None,
    )
    recommended_action = llm_result.get("recommended_action") or get_recommended_action(risk_level)

    return {
        "raw_text": text,
        "score": score,
        "risk_level": risk_level,
        "ml_prediction": ml_result["prediction"],
        "ml_confidence": ml_result.get("confidence"),
        "rule_score": rule_result["score"],
        "pattern_score": pattern_score,
        "matched_pattern": matched_pattern,  # real ScamPattern instance or None — safe for the FK
        "category": matched_pattern.get_category_display() if matched_pattern else "Unclassified",
        "evidence": _flatten_evidence(rule_result["evidence"]),
        "urls": rule_result.get("urls", []),
        "llm_explanation": llm_result["explanation"],
        "recommended_action": recommended_action,
    }