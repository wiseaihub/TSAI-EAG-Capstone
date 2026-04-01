from pydantic import BaseModel, Field


class KbSaveRequest(BaseModel):
    role: str = Field(..., description="Caller role: patient|doctor")
    layer: str = Field(..., description="KB layer: web_research|product_kb|doctor_context|patient_context")
    title: str | None = Field(None, max_length=240)
    content: str = Field(..., min_length=1, max_length=20000)
    tags: list[str] | None = None
    source_type: str | None = Field(None, max_length=64)
    source_url: str | None = Field(None, max_length=2000)
    source_domain: str | None = Field(None, max_length=240)
    source_ref: dict | None = None
    metadata: dict | None = None
    is_shared: bool = False
    base_confidence: float | None = Field(None, ge=0.0, le=1.0)


class KbSaveResponse(BaseModel):
    id: str
    confidence: float


class KbQueryRequest(BaseModel):
    role: str = Field(..., description="Caller role: patient|doctor")
    query_text: str = Field(..., min_length=1, max_length=2000)
    layer_order: list[str] | None = None
    layers: list[str] | None = None
    limit: int = Field(10, ge=1, le=50)
    source_domain: str | None = None
    tags_any: list[str] | None = None


class KbQueryResult(BaseModel):
    id: str
    layer: str
    title: str | None
    content: str
    source_url: str | None
    source_domain: str | None
    tags: list[str] | None
    metadata: dict | None
    confidence: float


class KbQueryResponse(BaseModel):
    results: list[KbQueryResult]
    response_confidence: float


class KbFeedbackRequest(BaseModel):
    role: str = Field(..., description="Caller role: patient|doctor")
    entry_id: str
    rating: int = Field(..., ge=1, le=5)
    comment: str | None = Field(None, max_length=2000)
    correction: str | None = Field(None, max_length=4000)


class KbFeedbackResponse(BaseModel):
    entry_id: str
    confidence_before: float
    confidence_after: float
