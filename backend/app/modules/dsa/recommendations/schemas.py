from pydantic import BaseModel


class ProblemRecommendation(BaseModel):
    problem_id: int
    title: str
    difficulty: str | None
    rating: int | None
    score: float
    reason: str
