from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.modules.dsa.progress.models import UserProblemProgress
from app.modules.dsa.progress.schemas import (
    ProgressResponse,
    OverallProgressResponse,
    TopicProgressResponse,
)
from app.modules.dsa.progress.service import (
    get_overall_progress,
    get_topic_progress,
    get_weak_topics,
)
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


@router.get(
    "/summary",
    response_model=OverallProgressResponse
)
def get_progress_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_overall_progress(
        current_user.id,
        db
    )


@router.get(
    "/topics",
    response_model=list[TopicProgressResponse]
)
def get_progress_by_topic(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_topic_progress(
        current_user.id,
        db
    )


@router.get(
    "/weak-topics",
    response_model=list[TopicProgressResponse]
)
def get_weak_topic_list(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_weak_topics(
        current_user.id,
        db
    )
