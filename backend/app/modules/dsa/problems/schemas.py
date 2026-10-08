from pydantic import BaseModel, Field


class PlatformCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)


class PlatformResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class ProblemCreate(BaseModel):
    platform_id: int
    external_id: str = Field(min_length=1, max_length=100)
    title: str = Field(min_length=1, max_length=255)
    url: str = Field(min_length=1, max_length=500)
    difficulty: str | None = None
    rating: int | None = None


class ProblemResponse(BaseModel):
    id: int
    platform_id: int
    external_id: str
    title: str
    url: str
    difficulty: str | None
    rating: int | None

    class Config:
        from_attributes = True
