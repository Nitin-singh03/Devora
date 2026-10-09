from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.dependencies import get_current_user

from app.modules.dsa.revisions.schemas import RevisionResponse
from app.modules.dsa.revisions.service import get_due_revisions


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
