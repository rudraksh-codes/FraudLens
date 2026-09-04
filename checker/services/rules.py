# checker/services/rules.py
import re
from urllib.parse import urlparse

URGENT_PATTERNS = [
    r"\burgent\b", r"\bimmediately\b", r"\bact now\b", r"\baction required\b",
    r"\blast warning\b", r"\bfinal notice\b", r"\bwithin \d+ hours?\b",
    r"\bwithin \d+ minutes?\b", r"\bexpires? (today|soon)\b",
]

CREDENTIAL_PATTERNS = [
    r"\botp\b", r"\bpassword\b", r"\bpasscode\b", r"\bpin\b", r"\bcvv\b",
    r"\bcard number\b", r"\baccount number\b", r"\bverify your account\b",
    r"\bverify your identity\b", r"\bkyc\b", r"\bupdate kyc\b",
    r"\bpan card\b", r"\baadhaar\b",
]

MONEY_PATTERNS = [
    r"\bpay\b", r"\bpayment\b", r"\bprocessing fee\b", r"\bdeposit\b",
    r"\btransfer\b", r"\bcashback\b", r"\breward\b", r"\bprize\b",
    r"\bbonus\b", r"\bloan\b", r"\brefund\b", r"\bupi\b",
]

THREAT_PATTERNS = [
    r"\baccount.*blocked\b", r"\baccount.*suspend", r"\baccount.*closed\b",
    r"\bcard.*blocked\b", r"\bsim.*deactivat", r"\belectricity.*disconnect",
    r"\blegal action\b", r"\bpolice action\b", r"\barrest\b",
]

PROMOTIONAL_PATTERNS = [
    r"\bfree\b", r"\bwon\b", r"\bwinner\b", r"\bcongratulations\b",
    r"\blimited offer\b", r"\blimited time\b", r"\bexclusive offer\b",
]

# Matches full http(s)/www URLs AND bare shortener/domain patterns
URL_REGEX = re.compile(
    r"(https?://[^\s]+"
    r"|www\.[^\s]+"
    r"|\b[a-z0-9-]+\.(?:com|in|co|net|org|xyz|info|link|ly|me|shop|online|site)(?:/[^\s]*)?)",
    re.IGNORECASE,
)


def _find_matches(text: str, patterns: list[str]) -> list[str]:
    found = []
    for pattern in patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            found.append(m.group(0))
    return found


def extract_urls(text: str) -> list[str]:
    urls = URL_REGEX.findall(text)
    # strip trailing sentence punctuation the regex can accidentally grab
    return [u.rstrip(".,;:!?)") for u in urls]


def check_url_signals(url: str) -> dict:
    normalized = url.strip()
    if normalized.startswith("www."):
        normalized = "https://" + normalized
    elif not normalized.startswith(("http://", "https://")):
        normalized = "https://" + normalized  # bare domain, e.g. bit.ly/xyz

    try:
        parsed = urlparse(normalized)
    except ValueError:
        return {"score": 0, "evidence": []}

    hostname = (parsed.hostname or "").lower()
    evidence = []
    score = 0

    if url.strip().startswith("http://"):
        score += 10
        evidence.append("URL does not use HTTPS")
    if "@" in normalized:
        score += 15
        evidence.append("URL contains an @ symbol")
    if len(normalized) > 100:
        score += 10
        evidence.append("Unusually long URL")
    if hostname.count(".") >= 3:
        score += 10
        evidence.append("URL has many subdomains")

    for term in ["verify", "login", "secure", "account", "update", "kyc", "claim", "reward", "bank", "wallet", "payment", "bonus"]:
        if term in hostname:
            score += 5
            evidence.append(f"URL contains suspicious term: {term}")

    return {"score": min(score, 40), "evidence": evidence}


def check_rules(text: str) -> dict:
    text = text.strip()
    score = 0
    evidence = []

    urls = extract_urls(text)

    for label, patterns, weight, cap, message in [
        ("urgency", URGENT_PATTERNS, 70, 20, "Urgency or time-pressure language detected"),
        ("credential_request", CREDENTIAL_PATTERNS, 70, 30, "Credential or identity-verification language detected"),
        ("financial_signal", MONEY_PATTERNS, 75, 20, "Financial transaction or reward language detected"),
        ("threat", THREAT_PATTERNS, 70, 25, "Threat or consequence language detected"),
        ("promotion", PROMOTIONAL_PATTERNS, 70, 15, "Prize, reward, or promotional language detected"),
    ]:
        matches = _find_matches(text, patterns)
        if matches:
            score += min(len(matches) * weight, cap)
            evidence.append({"type": label, "message": message, "matches": matches})

    url_evidence = []
    for url in urls:
        result = check_url_signals(url)
        score += result["score"]
        url_evidence.extend(result["evidence"])

    if urls:
        evidence.append({
            "type": "url",
            "message": f"{len(urls)} link(s) detected",
            "matches": urls,
            "url_signals": url_evidence,
        })

    return {"score": min(score, 100), "evidence": evidence, "urls": urls}