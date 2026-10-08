from datetime import datetime

from pydantic import BaseModel


class ProgressResponse(BaseModel):
    id: int
    user_id: int
    problem_id: int
    status: str
    attempts: int
    last_status: str | None
    last_attempted_at: datetime | None
    first_solved_at: datetime | None
    last_solved_at: datetime | None

    class Config:
        from_attributes = True


class OverallProgressResponse(BaseModel):
    attempted: int
    solved: int
    submissions: int
    success_rate: float


class TopicProgressResponse(BaseModel):
    topic_id: int
    topic: str
    attempted: int
    solved: int
    success_rate: float
