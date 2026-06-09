from pydantic import BaseModel, Field
from typing import List, Literal


class ContextDoc(BaseModel):
    id: str
    text: str = Field(
        max_length=20000
    )


class Metadata(BaseModel):
    app_id: str
    user_id: str
    request_id: str


class AnalyzeRequest(BaseModel):
    prompt: str = Field(
        min_length=1,
        max_length=20000
    )

    context_docs: List[ContextDoc] = Field(
        default_factory=list,
        max_length=3
    )

    metadata: Metadata


class Reason(BaseModel):
    tag: str
    evidence: str


class AnalyzeResponse(BaseModel):
    decision: Literal[
        "allow",
        "transform",
        "block"
    ]

    risk_score: int = Field(
        ge=0,
        le=100
    )

    risk_tags: List[str]

    sanitized_prompt: str

    sanitized_context_docs: List[
        ContextDoc
    ]

    reasons: List[Reason]