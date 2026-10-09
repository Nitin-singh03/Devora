from datetime import datetime
from pydantic import BaseModel, Field


class RevisionResponse(BaseModel):
    id: int
    problem_id: int
    revision_count: int
    confidence: int
    last_revision_at: datetime | None
    next_revision_at: datetime | None

    class Config:
        from_attributes = True


class RevisionSubmit(BaseModel):
    confidence: int = Field(
        ge=1,
        le=5
    )
