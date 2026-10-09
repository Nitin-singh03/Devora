from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.dependencies import get_current_user

from app.modules.dsa.revisions.schemas import (
    RevisionResponse,
    RevisionSubmit
)
from app.modules.dsa.revisions.service import (
    get_due_revisions,
    submit_revision
)


router = APIRouter(
    prefix="/api/revisions",
    tags=["Revisions"]
)


@router.get(
    "/today",
    response_model=list[RevisionResponse]
)
def today_revisions(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_due_revisions(
        current_user.id,
        db
    )


@router.post(
    "/{problem_id}/submit",
    response_model=RevisionResponse
)
def submit_problem_revision(
    problem_id: int,
    data: RevisionSubmit,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    revision = submit_revision(
        current_user.id,
        problem_id,
        data.confidence,
        db
    )

    if not revision:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Revision not found"
        )

    return revision
