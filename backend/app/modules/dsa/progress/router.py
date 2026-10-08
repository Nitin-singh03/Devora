from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.modules.dsa.progress.models import UserProblemProgress
from app.modules.dsa.progress.schemas import ProgressResponse
from app.modules.users.models import User


router = APIRouter(
    prefix="/api/progress",
    tags=["Progress"]
)


@router.get(
    "",
    response_model=list[ProgressResponse]
)
def get_my_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(UserProblemProgress).filter(
        UserProblemProgress.user_id == current_user.id
    ).order_by(
        UserProblemProgress.updated_at.desc()
    ).all()
