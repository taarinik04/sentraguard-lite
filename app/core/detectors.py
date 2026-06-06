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
    "reveal secrets"
]


# PII Patterns


EMAIL_REGEX = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

PHONE_REGEX = r"\b\d{10}\b"



# Prompt Injection Detector


def detect_prompt_injection(text):
    findings = []

    for phrase in PROMPT_INJECTION_PATTERNS:
        if phrase.lower() in text.lower():
            findings.append(phrase)

    return findings



# PII Detector


def detect_pii(text):

    emails = re.findall(
        EMAIL_REGEX,
        text
    )

    phones = re.findall(
        PHONE_REGEX,
        text
    )

    return emails, phones



# PII Redaction


def redact_pii(text):

    text = re.sub(
        EMAIL_REGEX,
        "[REDACTED_EMAIL]",
        text
    )

    text = re.sub(
        PHONE_REGEX,
        "[REDACTED_PHONE]",
        text
    )

    return text



# RAG Injection Detector


def detect_rag_injection(context_docs):

    findings = []

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