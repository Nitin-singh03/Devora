from app.modules.dsa.problems.models import Problem
from app.modules.dsa.submissions.models import Submission


def create_submission(
    user_id: int,
    data,
    db
):
    problem = db.query(Problem).filter(
        Problem.id == data.problem_id
    ).first()

    if not problem:
        return None, "Problem not found"

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
    db.commit()
    db.refresh(submission)

    return submission, None
