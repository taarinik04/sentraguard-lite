# Design Notes – SentraGuard Lite

## Problem Statement

The goal of this project was to develop a lightweight guardrails gateway that evaluates prompts before they are sent to a Large Language Model (LLM).

The system focuses on detecting three major categories of risk:

* Prompt Injection
* Personally Identifiable Information (PII)
* RAG Injection

The gateway analyzes detected risks, computes a risk score, and returns a policy decision.

---

## Detection Approach

A rule-based detection strategy was selected instead of a machine-learning approach.

This decision was made because a rule-based system provides:

* Simpler implementation
* Faster execution
* Easier debugging
* Deterministic and reproducible results

Since the assignment focuses on guardrails and policy enforcement rather than model training, pattern matching was an appropriate solution.

---

## Technology Choices

### FastAPI

FastAPI was selected because it provides:

* Automatic request validation using Pydantic
* High performance and low overhead
* Simple endpoint creation
* Strong typing support
* Easy deployment

The framework allows the API layer to remain lightweight and maintainable.

### Streamlit

Streamlit was chosen to provide a simple web interface without requiring a dedicated frontend framework.

This enabled rapid development of an interactive interface for prompt analysis and result visualization.

### Docker

Docker support was added to ensure consistent execution across different environments without requiring manual dependency installation.

---

## Risk Scoring Design

The system uses a weighted risk-scoring model.

When a detector is triggered, a predefined score is added to the total risk score.

| Risk Type        | Score |
| ---------------- | ----- |
| Prompt Injection | 50    |
| PII              | 30    |
| RAG Injection    | 40    |

The final score is calculated by summing all triggered risk categories.

This approach was selected because it is easy to explain, test, audit, and modify.

---

## Decision Policy

The system currently supports three policy decisions:

| Score Range | Decision  |
| ----------- | --------- |
| 0–39        | Allow     |
| 40–79       | Transform |
| 80+         | Block     |

In addition, high-confidence prompt injection patterns can trigger an immediate block decision.

This policy ensures that moderate-risk content is sanitized before use, while highly suspicious content is prevented from reaching downstream systems.

---

## Tradeoffs

### Simplicity vs Coverage

The system prioritizes simplicity and explainability over maximum detection coverage.

More sophisticated detection techniques could identify additional attack patterns but would increase implementation complexity and maintenance requirements.

### Explainability vs Intelligence

Pattern-based detection produces results that are easy to understand and justify.

Machine-learning-based approaches may improve detection accuracy but are generally less transparent and require additional computational resources and maintenance effort.

---

## Limitations

The current implementation has several limitations:

* Detection is limited to predefined patterns and keywords
* Only email addresses and phone numbers are currently treated as PII
* Context analysis relies primarily on keyword matching
* Authentication is not implemented
* Persistent storage is not implemented
* Audit logging is limited to application-level logs

These limitations were accepted to keep the project aligned with the scope of the assignment.

---

## Future Improvements

Potential future enhancements include:

* Machine-learning-assisted prompt injection detection
* Support for additional PII categories such as addresses and government identifiers
* Configurable scoring policies and detector thresholds
* Authentication and API key management
* Structured audit logging and monitoring
* Rate limiting and abuse detection
* SIEM integration
* Historical analysis dashboards
* Advanced validation for vector database and RAG pipelines

---

## Testing Strategy

Automated tests are included to validate both positive and negative scenarios.

Testing focuses on:

* API behavior
* Prompt injection detection
* RAG injection detection
* PII detection and redaction
* Risk scoring
* Response validation
* Input validation
* Security policy enforcement
* Edge cases and error handling

The test suite helps ensure that changes can be verified quickly and consistently without extensive manual testing.
