from pydantic import BaseModel
from typing import List, Optional


class ContextDoc(BaseModel):
    id: str
    text: str


class Metadata(BaseModel):
    app_id: Optional[str] = None
    user_id: Optional[str] = None
    request_id: Optional[str] = None


class AnalyzeRequest(BaseModel):
    prompt: str
    context_docs: List[ContextDoc] = []
    metadata: Metadata


class Reason(BaseModel):
    tag: str
    evidence: str


class AnalyzeResponse(BaseModel):
    decision: str
    risk_score: int
    risk_tags: List[str]
    sanitized_prompt: str
    sanitized_context_docs: List[ContextDoc]
    reasons: List[Reason]