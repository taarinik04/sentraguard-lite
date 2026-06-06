# SentraGuard Lite

The project has been created for the internship assignment of the Sovereign AI programme.

SentraGuard Lite is a lightweight GenAI guardrails gateway that filters incoming prompts, and optionally retrieved context prior to an LLM. Common prompt injection attempts, PII (Personally Identifiable Information) and suspicious instructions within retrieved documents are identified by the system. It uses the results to assign a risk score, and then returns a policy decision.

---

# Features

Currently the gateway supports:

* Prompt Injection Detection
* PII Detection and Redaction
* RAG Injection Detection
* Risk Scoring
* Prompt Sanitization
* FastAPI REST API
* Streamlit Web Interface
* CLI Interface
It discusses about Automated testing using pytest.
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
│   ├── storage/
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

Set up and enable a virtual environment:

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

# Running the API

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

API URL:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
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
Include optional context documents
* Analyze prompt risk
View risk score & tags
* View sanitized output
Next, check the raw JSON response.Then, look at the raw JSON response.

---

# Running the CLI

The running API communicates with the CLI, which stores the analyses result to a file.

Command:

```bash
python cli.py analyze --input sample_request.json --output out.json
```

Example output:

```text
Analysis Complete
Input  : sample_request.json
Output : out.json
```

Example generated file:

```json
{
  "decision": "transform",
  "risk_score": 50,
  "risk_tags": [
    "prompt_injection"
  ],
  "sanitized_prompt": "Ignore previous instructions",
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

# Running Tests

Execute:

```bash
pytest -v
```

Expected result:

```text
10 passed
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

No configuration needed.

---

# API Endpoints

## POST /analyze

Interprets prompt and optional context retrieved.

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
  "decision": "transform",
  "risk_score": 50,
  "risk_tags": [
    "prompt_injection"
  ],
  "sanitized_prompt": "Ignore previous instructions"
}
```

---

## GET /policy

Gets the current configuration of the active detector.

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

# Design Notes

## Assumptions

The system runs completely without Internet and connection.
No external LLM APIs needed!
The assignment can be accomplished using a rule-based approach.
Retrieval documents are trusted inputs, unless verifying for RAG injection patterns.

## Tradeoffs

Use of Pattern matching instead of ML-based was selected to ensure that implementation is lightweight and deterministic and easy to test.
In-memory processing (no infrastructure) was used to avoid infrastructure complexity.
The scoring system is kept deliberately simple and "plainspoken.

## Limitations

Detection can only happen for pre-defined phrases and patterns.
Only Name+Email Address (and phone numbers) considered as PII.
No learning is implemented in the system at the moment.
No persistent audit or authentication is done.

## Future Improvements

Add support for describe-classification via classification using ML.
Include other PII categories including addresses, IDs.
Implementable policies and thresholds can be set up.
Implement authentication and audit logging:
Archive results of analysis for reporting and monitoring.

---

# AI Usage Note

AI assisted tools have been utilized for certain development activities including:

Copy and paste boilerplate to create the initial project scaffolding.
Apply Regular Expressions to check if data elements contain sensitive information.Apply Regular Expressions to validate PII data.
Tutorials on how to troubleshoot and setup Docker
* Documentation formatting suggestions

All this, from implementation to testing, debugging, integration to end validation testing, was done manually. The solution submitted was reviewed, modified and tested end to end prior to submission.

---

## Author

**Taarini Kumar**


GitHub: https://github.com/taarinik04
