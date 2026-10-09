from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.dependencies import get_current_user
from app.modules.dsa.planner.schemas import StudyPlanResponse
from app.modules.dsa.planner.service import create_study_plan
from app.modules.users.models import User


router = APIRouter(
    prefix="/api/planner",
    tags=["Planner"]
)


@router.get(
    "",
    response_model=StudyPlanResponse
)
@router.get(
    "/today",
    response_model=StudyPlanResponse
)
def get_today_plan(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_study_plan(
        current_user.id,
        db
    )
