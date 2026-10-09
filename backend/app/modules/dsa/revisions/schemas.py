from datetime import datetime
from pydantic import BaseModel


class RevisionResponse(BaseModel):
    id: int
    problem_id: int
    revision_count: int
    confidence: int
    last_revision_at: datetime | None
    next_revision_at: datetime | None

    class Config:
        from_attributes = True
