import base64
import html
import re
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple

ATTACK_PATTERNS = {
    "Instruction Override": [r"ignore (all )?(previous|prior|system) instructions", r"forget your instructions", r"override developer"],
    "Role Change": [r"you are now", r"act as", r"pretend to be", r"switch role"],
    "Secret Extraction": [r"reveal.*(secret|api key|token|password)", r"print.*(system prompt|hidden prompt)", r"show me.*credentials", r"hidden api key", r"any bearer token", r"secret"],
    "Tool Abuse": [r"send email", r"delete .*files?", r"transfer money", r"call .*api", r"execute shell"],
    "Credential Theft": [r"api[_ -]?key", r"password", r"oauth", r"bearer token", r"private key"],
    "Context Poisoning": [r"add this to memory", r"store this instruction", r"from now on", r"always obey"],
    "Multi-Step Jailbreaks": [r"step 1.*step 2", r"first.*then.*finally", r"multi[- ]?step"],
    "Encoded Instructions": [r"base64", r"decode this", r"rot13", r"hex encoded", r"atob\("],
    "Indirect Prompt Injection": [r"<!--.*ignore.*-->", r"hidden instruction", r"for ai agents only", r"crawler instruction"],
}

CANARY_SECRETS = ["CANARY_API_KEY_X7", "CANARY_CUSTOMER_TOKEN_92", "CANARY_PAYROLL_SECRET_11"]

@dataclass
class DetectionResult:
    source_type: str
    decision: str
    risk_score: int
    attack_types: List[str]
    evidence: List[str]
    sanitized_content: str
    recommended_action: str
    confidence: int


def _try_decode_base64(text: str) -> List[str]:
    candidates = re.findall(r"[A-Za-z0-9+/=]{24,}", text)
    decoded = []
    for c in candidates[:5]:
        try:
            value = base64.b64decode(c + "===").decode("utf-8", errors="ignore")
            if len(value.strip()) > 8:
                decoded.append(value)
        except Exception:
            pass
    return decoded


def normalize_content(content: str) -> str:
    content = html.unescape(content or "")
    content = re.sub(r"<script.*?</script>", " ", content, flags=re.I | re.S)
    content = re.sub(r"<style.*?</style>", " ", content, flags=re.I | re.S)
    content = re.sub(r"<[^>]+>", " ", content)
    return re.sub(r"\s+", " ", content).strip()


def detect_prompt_injection(content: str, source_type: str = "user_message") -> DetectionResult:
    original = content or ""
    normalized = normalize_content(original)
    inspection_texts: List[Tuple[str, str]] = [("original/normalized", original + "\n" + normalized)]
    for decoded in _try_decode_base64(original):
        inspection_texts.append(("decoded_base64", decoded))

    attack_types = []
    evidence = []
    lower_blob = "\n".join(t for _, t in inspection_texts).lower()

    for attack, patterns in ATTACK_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, lower_blob, flags=re.I | re.S):
                attack_types.append(attack)
                evidence.append(f"{attack}: matched pattern `{pattern}`")
                break

    for secret in CANARY_SECRETS:
        if secret.lower() in lower_blob:
            if "Secret Extraction" not in attack_types:
                attack_types.append("Secret Extraction")
            evidence.append(f"Canary secret touched: {secret}")

    unique_attacks = list(dict.fromkeys(attack_types))
    risk = min(100, len(unique_attacks) * 24 + (20 if "Secret Extraction" in unique_attacks else 0) + (15 if "Tool Abuse" in unique_attacks else 0))

    if risk >= 70:
        decision = "BLOCK"
        action = "Quarantine content and prevent downstream agent/tool execution."
    elif risk >= 20:
        decision = "SANITIZE"
        action = "Remove external instructions and forward safe factual content only."
    else:
        decision = "ALLOW"
        action = "Forward content with normal monitoring."

    sanitized = normalized
    if decision in {"SANITIZE", "BLOCK"}:
        sanitized = re.sub(r"(?i)ignore .*?(instructions|prompt)", "[REMOVED INSTRUCTION OVERRIDE]", sanitized)
        sanitized = re.sub(r"(?i)(send email|delete files|reveal secret|api key|password).*", "[REMOVED UNSAFE ACTION REQUEST]", sanitized)
        for secret in CANARY_SECRETS:
            sanitized = sanitized.replace(secret, "[REDACTED_CANARY]")

    confidence = min(98, 60 + len(unique_attacks) * 7 + (10 if risk >= 70 else 0))
    if not unique_attacks:
        confidence = 86

    return DetectionResult(
        source_type=source_type,
        decision=decision,
        risk_score=risk,
        attack_types=unique_attacks,
        evidence=evidence or ["No malicious instruction patterns detected."],
        sanitized_content=sanitized,
        recommended_action=action,
        confidence=confidence,
    )


def result_to_dict(result: DetectionResult) -> Dict:
    return asdict(result)
