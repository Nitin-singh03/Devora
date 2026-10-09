from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.modules.dsa.revisions.models import ProblemRevision


BASE_INTERVALS = [
    1,
    3,
    7,
    14,
    30,
    60
]


def calculate_next_revision(
    revision_count: int,
    confidence: int = 1
):
    index = min(
        revision_count,
        len(BASE_INTERVALS) - 1
    )

    base_days = BASE_INTERVALS[index]

    if confidence <= 2:
        days = max(1, base_days // 2)

    elif confidence == 3:
        days = base_days

    elif confidence == 4:
        days = int(base_days * 1.5)

    else:
        days = base_days * 2

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
        revision.revision_count - 1,
        revision.confidence
    )

    db.commit()
    db.refresh(revision)

    return revision


def submit_revision(
    user_id: int,
    problem_id: int,
    confidence: int,
    db: Session
):
    revision = db.query(ProblemRevision).filter(
        ProblemRevision.user_id == user_id,
        ProblemRevision.problem_id == problem_id
    ).first()

    if not revision:
        return None

    revision.confidence = confidence

    revision.revision_count += 1

    revision.last_revision_at = datetime.utcnow()

    revision.next_revision_at = calculate_next_revision(
        revision.revision_count - 1,
        confidence
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
