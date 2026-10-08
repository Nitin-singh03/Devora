from pydantic import BaseModel, Field


class TopicCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100
    )


class TopicResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
