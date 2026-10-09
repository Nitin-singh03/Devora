from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.modules.dsa.revisions.models import ProblemRevision


REVISION_INTERVALS = [
    1,
    3,
    7,
    14,
    30,
    60
]


def calculate_next_revision(revision_count: int):
    index = min(
        revision_count,
        len(REVISION_INTERVALS) - 1
    )

    days = REVISION_INTERVALS[index]

    return datetime.utcnow() + timedelta(days=days)


def create_or_update_revision(
    user_id: int,
    problem_id: int,
    db: Session
):
    revision = db.query(ProblemRevision).filter(
        ProblemRevision.user_id == user_id,
        ProblemRevision.problem_id == problem_id
    ).first()

    now = datetime.utcnow()

    if not revision:
        revision = ProblemRevision(
            user_id=user_id,
            problem_id=problem_id,
            revision_count=0,
            confidence=1
        )

        db.add(revision)

    revision.revision_count += 1
    revision.last_revision_at = now
    revision.next_revision_at = calculate_next_revision(
        revision.revision_count - 1
    )

    db.commit()
    db.refresh(revision)

    return revision


def get_due_revisions(
    user_id: int,
    db: Session
):
    now = datetime.utcnow()

    return db.query(ProblemRevision).filter(
        ProblemRevision.user_id == user_id,
        ProblemRevision.next_revision_at <= now
    ).order_by(
        ProblemRevision.next_revision_at
    ).all()
