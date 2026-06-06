from fastapi import FastAPI

from app.schemas import (
    AnalyzeRequest,
    AnalyzeResponse
)

from app.core.analyzer import analyze_request


app = FastAPI(
    title="SentraGuard Lite",
    description="Minimal GenAI Guardrails Gateway",
    version="1.0"
)


@app.post(
    "/analyze",
    response_model=AnalyzeResponse
)
def analyze(data: AnalyzeRequest):

    result = analyze_request(
        data.prompt,
        data.context_docs
    )

    return result


@app.get("/policy")
def get_policy():

    return {
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