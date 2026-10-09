from sqlalchemy.orm import Session

from app.modules.dsa.revisions.service import get_due_revisions
from app.modules.dsa.recommendations.service import get_recommendations
from app.modules.dsa.problems.models import Problem


def create_study_plan(
    user_id: int,
    db: Session
):
    plan = []

    # 1. Revisions first
    revisions = get_due_revisions(
        user_id,
        db
    )

    for revision in revisions:

        problem = db.query(Problem).filter(
            Problem.id == revision.problem_id
        ).first()

        if problem:
            plan.append({
                "problem_id": problem.id,
                "title": problem.title,
                "type": "revision",
                "priority": 100
            })

    # 2. New recommendations
    recommendations = get_recommendations(
        user_id,
        db,
        limit=5
    )

    for recommendation in recommendations:

        plan.append({
            "problem_id": recommendation["problem_id"],
            "title": recommendation["title"],
            "type": "practice",
            "priority": int(
                recommendation["score"]
            )
        })

    plan.sort(
        key=lambda x: x["priority"],
        reverse=True
    )

    return {
        "items": plan[:10]
    }
