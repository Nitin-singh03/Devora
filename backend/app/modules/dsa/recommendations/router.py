from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db

from app.modules.dsa.recommendations.schemas import (
    ProblemRecommendation
)

from app.modules.dsa.recommendations.service import (
    get_recommendations
)

from app.modules.users.models import User


router = APIRouter(
    prefix="/api/recommendations",
    tags=["Recommendations"]
)


@router.get(
    "/problems",
    response_model=list[ProblemRecommendation]
)
def recommend_problems(
    goal: str = Query(
        "interview",
        description="Recommendation goal: 'interview', 'contest', or 'revision'"
    ),
    limit: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_recommendations(
        current_user.id,
        db,
        goal=goal,
        limit=limit
    )

