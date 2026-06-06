from app.core.detectors import (
    detect_prompt_injection,
    detect_pii,
    redact_pii,
    detect_rag_injection
)


def analyze_request(prompt, contextdocs):

    rscore = 0
    rtags = []
    reasons = []

    sanitizedprompt = prompt

    sanitized_contextdocs = contextdocs

    # Prompt Injection Detection
    prompt_hits = detect_prompt_injection(prompt)

    if prompt_hits:
        rscore += 50
        rtags.append("prompt_injection")

        for hit in prompt_hits:
            reasons.append(
                {
                    "tag": "prompt_injection",
                    "evidence": f"matched phrase: {hit}"
                }
            )

    # PII Detection
    emails, phones = detect_pii(prompt)

    if emails or phones:
        rscore += 30
        rtags.append("pii")

        sanitizedprompt = redact_pii(prompt)

        reasons.append(
            {
                "tag": "pii",
                "evidence": "email or phone detected"
            }
        )

    # RAG Injection Detection
    rag_hits = detect_rag_injection(contextdocs)

    if rag_hits:
        rscore += 40
        rtags.append("rag_injection")

        reasons.append(
            {
                "tag": "rag_injection",
                "evidence": str(rag_hits[0])
            }
        )

    # Decision Logic
    if rscore >= 80:
        decision = "block"
    elif rscore >= 40:
        decision = "transform"
    else:
        decision = "allow"

    return {
        "decision": decision,
        "risk_score": rscore,
        "risk_tags": list(set(rtags)),
        "sanitized_prompt": sanitizedprompt,
        "sanitized_context_docs": sanitized_contextdocs,
        "reasons": reasons
    }