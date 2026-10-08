from datetime import datetime

from pydantic import BaseModel, Field


class SubmissionCreate(BaseModel):
    problem_id: int
    status: str = Field(min_length=1, max_length=50)
    language: str | None = Field(
        default=None,
        max_length=50
    )
    runtime: int | None = None
    memory: int | None = None
    source: str = Field(
        default="manual",
        max_length=50
    )


class SubmissionResponse(BaseModel):
    id: int
    user_id: int
    problem_id: int
    status: str
    language: str | None
    runtime: int | None
    memory: int | None
    submitted_at: datetime
    source: str

    class Config:
        from_attributes = True
