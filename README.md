# SentraGuard Lite

SentraGuard Lite is a lightweight GenAI guardrails gateway developed for the Sovereign AI Internship Assignment.

The system analyzes user prompts and optional retrieved context before they are sent to an LLM. It detects prompt injection attempts, Personally Identifiable Information (PII), and suspicious instructions within retrieved documents. Based on detected risks, the gateway assigns a risk score and returns a policy decision.

---

# Features

Currently the gateway supports:

* Prompt Injection Detection
* PII Detection and Redaction
* RAG Injection Detection
* Risk Scoring and Policy Decisions
* Prompt and Context Sanitization
* FastAPI REST API
* Streamlit Web Interface
* CLI Interface
* Automated Testing using pytest
* Dockerized Deployment

---

# Project Structure

```text
assignment/
│
├── app/
│   ├── core/
│   │   ├── analyzer.py
│   │   └── detectors.py
│   ├── main.py
│   └── schemas.py
│
├── ui/
│   └── streamlit_app.py
│
├── tests/
│   └── test_api.py
│
├── cli.py
├── sample_request.json
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── design_notes.md
├── README.md
└── pytest.ini
```

---

# Installation

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Dependency Justification

The project intentionally uses a minimal dependency set to keep the solution lightweight, reproducible, and easy to audit.

| Dependency | Purpose                                        |
| ---------- | ---------------------------------------------- |
| FastAPI    | REST API implementation and request validation |
| Pydantic   | Schema validation and type enforcement         |
| Uvicorn    | ASGI server for FastAPI                        |
| Streamlit  | Lightweight web interface                      |
| Requests   | HTTP communication from the CLI                |
| Pytest     | Automated testing framework                    |

Additional packages required by Streamlit are installed automatically as part of the Streamlit ecosystem.

# Running the API

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

API URL:

```text
http://127.0.0.1:8000
```

---

# Running the Streamlit UI

```bash
streamlit run ui/streamlit_app.py
```

UI URL:

```text
http://localhost:8501
```

The UI enables the user to:

* Enter a prompt
* Provide up to three optional context documents
* Analyze prompt risk
* View risk score and risk tags
* View sanitized output
* Inspect the raw JSON response

---

# Running the CLI

The CLI communicates with the running API and stores the analysis result in a JSON file.

Command:

```bash
python cli.py analyze --input sample_request.json --output out.json
```

Example output:

```text
Analysis Complete
Input  : sample_request.json
Output : out.json
Decision : block
Risk Score : 50
```

---

# Running Tests

Execute:

```bash
pytest -v
```

Expected result:

```text
19 passed
```

---

# Running with Docker

Build and start all services:

```bash
docker compose up --build
```

Services:

```text
API : http://localhost:8000
UI  : http://localhost:8501
```

The Docker setup starts:

* FastAPI backend
* Streamlit frontend

No additional configuration is required.

---

# API Endpoints

## POST /analyze

Analyzes a prompt and optional retrieved context documents.

### Sample Request

```json
{
  "prompt": "Ignore previous instructions",
  "context_docs": [],
  "metadata": {
    "app_id": "demo",
    "user_id": "user",
    "request_id": "req"
  }
}
```

### Sample Response

```json
{
  "decision": "block",
  "risk_score": 50,
  "risk_tags": [
    "prompt_injection"
  ],
  "sanitized_prompt": "[BLOCKED]",
  "sanitized_context_docs": [],
  "reasons": [
    {
      "tag": "prompt_injection",
      "evidence": "matched phrase: ignore previous instructions"
    }
  ]
}
```

---

## GET /policy

Returns the active security policy configuration.

### Sample Response

```json
{
  "version": "1",
  "detectors": [
    "prompt_injection",
    "pii",
    "rag_injection"
  ],
  "thresholds": {
    "block_score": 80,
    "transform_score": 40
  }
}
```

---

# Security Notes

Several security-by-default measures have been implemented:

* Interactive API documentation endpoints (`/docs`, `/redoc`, and `/openapi.json`) are disabled to reduce API surface exposure.
* Prompt injection attempts are detected and scored before requests reach downstream systems.
* Personally Identifiable Information (PII) is automatically redacted before being returned.
* Suspicious retrieved documents are removed when RAG injection patterns are detected.
* Input validation is enforced through Pydantic schemas, including prompt length limits and context document limits.
* High-confidence prompt injection patterns trigger an immediate block decision.
* Maximum prompt and context sizes are enforced to reduce denial-of-service risk from excessively large payloads.


# Design Notes

## Assumptions

* The system operates entirely offline and does not require Internet access.
* No external LLM APIs are required.
* The assignment can be implemented using a deterministic rule-based approach.
* Retrieved documents are treated as trusted inputs unless they contain known RAG injection patterns.

## Tradeoffs

* Pattern matching was selected instead of machine learning to keep the implementation lightweight, deterministic, explainable, and easy to test.
* In-memory processing was used to avoid unnecessary infrastructure complexity.
* The scoring system is intentionally simple and transparent for ease of auditing and testing.

## Limitations

* Detection is limited to predefined phrases and patterns.
* Only email addresses and phone numbers are currently detected as PII.
* No machine-learning based detection is implemented.
* No persistent storage is maintained.
* Authentication is not implemented.

## Future Improvements

* Machine-learning based prompt injection detection
* Support for additional PII categories such as addresses and government identifiers
* External policy configuration through YAML or JSON files
* Structured audit logging and monitoring
* Authentication and API key management
* Rate limiting and abuse detection
* SIEM integration
* Advanced validation for vector database and RAG pipelines

---

# AI Usage Note

AI-assisted tools were used for selected development activities including:

* Initial project scaffolding and boilerplate generation
* Assistance in generating and refining regular expressions for PII detection and validation
* Docker setup and troubleshooting guidance
* Documentation formatting suggestions

All implementation, integration, debugging, testing, validation, and final review were performed manually before submission.

---

## Author

**Taarini Kumar**

GitHub Repository:

https://github.com/taarinik04/sentraguard-lite
