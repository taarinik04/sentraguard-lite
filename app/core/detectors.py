from typing import Any

import re


# Prompt Injection Detection

PROMPT_INJECTION_PATTERNS = [
    "ignore previous instructions",
    "reveal system prompt",
    "act as dan"
]


# RAG Injection Detection

RAG_PATTERNS = [
    "override policy",
    "ignore guidelines",
    "system:",
    "ignore previous instructions",
    "reveal secrets",
    "bypass restrictions",
    "disregard instructions"
]


# Scan Limits

MAX_SCAN_LENGTH = 20000


# PII Patterns

EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+"
    r"@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

PHONE_PATTERN = re.compile(
    r"(?:\+\d{1,3}[- ]?)?"
    r"(?:\(?\d{2,5}\)?[- ]?)?"
    r"\d{3,5}[- ]?\d{4,6}"
)


def detect_prompt_injection(
    text: str
) -> list[str]:
    """
    Detect known prompt injection phrases
    within a user prompt.

    Args:
        text: User-supplied prompt.

    Returns:
        List of matched prompt injection patterns.
    """

    findings: list[str] = []

    for phrase in PROMPT_INJECTION_PATTERNS:

        if phrase.lower() in text.lower():
            findings.append(phrase)

    return findings


def detect_pii(
    text: str
) -> tuple[list[str], list[str]]:
    """
    Detect email addresses and phone numbers
    within a text string.

    Args:
        text: User input text.

    Returns:
        Tuple containing:
        - list of emails
        - list of phone numbers
    """

    if len(text) > MAX_SCAN_LENGTH:
        return [], []

    emails = EMAIL_PATTERN.findall(text)

    phones = PHONE_PATTERN.findall(text)

    return emails, phones


def redact_pii(
    text: str
) -> str:
    """
    Replace detected email addresses and
    phone numbers with redaction tokens.

    Args:
        text: Original user input.

    Returns:
        Sanitized text with PII removed.
    """

    text = EMAIL_PATTERN.sub(
        "[REDACTED_EMAIL]",
        text
    )

    text = PHONE_PATTERN.sub(
        "[REDACTED_PHONE]",
        text
    )

    return text


def detect_rag_injection(
    context_docs: list[Any]
) -> list[dict[str, str]]:
    """
    Inspect retrieved context documents
    for RAG injection indicators.

    Args:
        context_docs: List of retrieved documents.

    Returns:
        List of detected RAG injection findings.
    """

    findings: list[dict[str, str]] = []

    for doc in context_docs:

        for pattern in RAG_PATTERNS:

            if pattern.lower() in doc.text.lower():

                findings.append(
                    {
                        "doc_id": doc.id,
                        "pattern": pattern
                    }
                )

    return findings