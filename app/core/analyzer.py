from typing import Any

import logging

from app.core.detectors import (
    detect_prompt_injection,
    detect_pii,
    redact_pii,
    detect_rag_injection
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger(__name__)


def analyze_request(
    prompt: str,
    contextdocs: list[Any]
) -> dict[str, Any]:
    """
    Analyze a user prompt and retrieved context documents
    for prompt injection, PII exposure, and RAG attacks.

    The function calculates a risk score, determines the
    appropriate decision (allow, transform, or block),
    sanitizes unsafe content, and returns supporting
    evidence for all detected findings.

    Args:
        prompt: User-supplied prompt.
        contextdocs: Retrieved context documents.

    Returns:
        Dictionary containing:
        - decision
        - risk_score
        - risk_tags
        - sanitized_prompt
        - sanitized_context_docs
        - reasons
    """

    risk_score = 0
    risk_tags = []
    reasons = []

    sanitized_prompt = prompt
    sanitized_context_docs = contextdocs

    # Prompt Injection Detection
    prompt_hits = detect_prompt_injection(prompt)

    high_confidence_pi = any(
        phrase in prompt.lower()
        for phrase in [
            "ignore previous instructions",
            "reveal system prompt"
        ]
    )

    if prompt_hits:
        risk_score += 50
        risk_tags.append("prompt_injection")

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
        risk_score += 30
        risk_tags.append("pii")

        sanitized_prompt = redact_pii(prompt)

        reasons.append(
            {
                "tag": "pii",
                "evidence": "email or phone detected"
            }
        )

    # RAG Injection Detection
    rag_hits = detect_rag_injection(contextdocs)

    if rag_hits:
        risk_score += 40
        risk_tags.append("rag_injection")

        sanitized_context_docs = []

        reasons.append(
            {
                "tag": "rag_injection",
                "evidence": str(rag_hits[0])
            }
        )

    # Decision Logic
    if high_confidence_pi:
        decision = "block"

        sanitized_prompt = "[BLOCKED]"
        sanitized_context_docs = []

    elif risk_score >= 80:
        decision = "block"

        sanitized_prompt = "[BLOCKED]"
        sanitized_context_docs = []

    elif risk_score >= 40:
        decision = "transform"

    else:
        decision = "allow"

    logger.info(
        "analysis_complete "
        f"decision={decision} "
        f"risk_score={risk_score} "
        f"risk_tags={list(set(risk_tags))}"
    )

    return {
        "decision": decision,
        "risk_score": risk_score,
        "risk_tags": list(set(risk_tags)),
        "sanitized_prompt": sanitized_prompt,
        "sanitized_context_docs": sanitized_context_docs,
        "reasons": reasons
    }