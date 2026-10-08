from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.modules.dsa.submissions.models import Submission
from app.modules.dsa.submissions.schemas import (
    SubmissionCreate,
    SubmissionResponse
)
from app.modules.dsa.submissions.service import (
    create_submission
)
from app.modules.users.models import User


router = APIRouter(
    prefix="/api/submissions",
    tags=["Submissions"]
)


@router.post(
    "",
    response_model=SubmissionResponse,
    status_code=status.HTTP_201_CREATED
)
def submit_problem(
    data: SubmissionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    submission, error = create_submission(
        current_user.id,
        data,
        db
    )

    if error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error
        )

    return submission


@router.get(
    "",
    response_model=list[SubmissionResponse]
)
def get_my_submissions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Submission).filter(
        Submission.user_id == current_user.id
    ).order_by(
        Submission.submitted_at.desc()
    ).all()
