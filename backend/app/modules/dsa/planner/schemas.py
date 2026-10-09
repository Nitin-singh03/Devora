from pydantic import BaseModel


class StudyPlanItem(BaseModel):
    problem_id: int
    title: str
    type: str
    priority: int


class StudyPlanResponse(BaseModel):
    items: list[StudyPlanItem]
