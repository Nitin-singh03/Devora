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
