
def calculate_score(rule_score: float, ml_result: dict, pattern_score: float) -> int:
    print(ml_result)
    ml_score = 0
    if ml_result.get("prediction") == "spam":
        # confidence = ml_result.get("confidence")
        # ml_score = confidence if confidence is not None else 60
        ml_score = 1 #simplifying

    score = (rule_score * 0.35) + (pattern_score * 0.30) + (ml_score * 0.35)
    return max(0, min(100, round(score)))


def get_risk_level(score: int) -> str:
    """Three tiers only — matches Submission.RISK_CHOICES and the
    risk-low/risk-medium/risk-high CSS classes already built. A fourth
    'CRITICAL' tier would save with no matching style or model choice."""
    if score < 5:
        return "LOW"
    if score < 30:
        return "MEDIUM"
    return "HIGH"


def get_recommended_action(risk_level: str) -> str:
    """Deterministic fallback used when the LLM call fails or times out."""
    actions = {
        "LOW": "No strong scam indicators were detected. Still verify the sender and context before acting.",
        "MEDIUM": "Proceed carefully. Do not share credentials or make payments until the message is independently verified.",
        "HIGH": "Do not click links, share OTPs or passwords, or make payments. Verify the sender through an official channel before taking any action.",
    }
    return actions[risk_level]  