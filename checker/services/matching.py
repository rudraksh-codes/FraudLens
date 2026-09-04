import re

from rapidfuzz import fuzz

from dashboard.models import ScamPattern  # adjust if ScamPattern lives elsewhere

MATCH_THRESHOLD = 75  # tune against real test messages before the final round


def normalize(text: str) -> str:
    """Must stay identical to the normalize() used in seed_patterns.py —
    if they drift apart, matching silently degrades. Consider importing
    this function into seed_patterns.py instead of keeping a second copy."""
    text = text.lower()
    text = re.sub(r"http\S+|www\.\S+", "<URL>", text)
    text = re.sub(r"[^\w\s<>]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def match_campaign(normalized_text: str):
    """Returns (ScamPattern instance, similarity 0-100) or (None, 0)."""
    best_pattern = None
    best_score = 0.0

    for pattern in ScamPattern.objects.all():
        score = fuzz.token_sort_ratio(normalized_text, pattern.normalized_text)
        if score > best_score:
            best_score = score
            best_pattern = pattern

    if best_pattern and best_score >= MATCH_THRESHOLD:
        return best_pattern, round(best_score, 2)

    return None, 0.0