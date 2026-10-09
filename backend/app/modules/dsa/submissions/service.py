from datetime import datetime

from app.modules.dsa.problems.models import Problem
from app.modules.dsa.submissions.models import Submission
from app.modules.dsa.progress.models import UserProblemProgress
from app.modules.dsa.revisions.service import create_or_update_revision


def create_submission(user_id: int, data, db):
    problem = db.query(Problem).filter(
        Problem.id == data.problem_id
    ).first()

    if not problem:
        return None, "Problem not found"

    now = datetime.utcnow()

    submission = Submission(
        user_id=user_id,
        problem_id=data.problem_id,
        status=data.status,
        language=data.language,
        runtime=data.runtime,
        memory=data.memory,
        source=data.source
    )

    db.add(submission)

    progress = db.query(UserProblemProgress).filter(
        UserProblemProgress.user_id == user_id,
        UserProblemProgress.problem_id == data.problem_id
    ).first()

    if not progress:
        progress = UserProblemProgress(
            user_id=user_id,
            problem_id=data.problem_id
        )
        db.add(progress)

    progress.attempts += 1
    progress.last_status = data.status
    progress.last_attempted_at = now

    if data.status.lower() == "accepted":
        if progress.first_solved_at is None:
            progress.first_solved_at = now

        progress.last_solved_at = now
        progress.status = "solved"

        create_or_update_revision(
            user_id=user_id,
            problem_id=data.problem_id,
            db=db
        )

    elif progress.status != "solved":
        progress.status = "attempted"

    db.commit()

    db.refresh(submission)
    db.refresh(progress)

    return submission, None
