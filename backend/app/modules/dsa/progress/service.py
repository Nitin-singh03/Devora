from sqlalchemy import func
from sqlalchemy.orm import Session

from app.modules.dsa.problems.models import Problem
from app.modules.dsa.progress.models import UserProblemProgress
from app.modules.dsa.submissions.models import Submission
from app.modules.dsa.topics.models import Topic
from app.modules.dsa.topics.problem_topics import ProblemTopic


def get_overall_progress(user_id: int, db: Session):

    attempted = db.query(
        func.count(UserProblemProgress.id)
    ).filter(
        UserProblemProgress.user_id == user_id
    ).scalar()

    solved = db.query(
        func.count(UserProblemProgress.id)
    ).filter(
        UserProblemProgress.user_id == user_id,
        UserProblemProgress.status == "solved"
    ).scalar()

    submissions = db.query(
        func.count(Submission.id)
    ).filter(
        Submission.user_id == user_id
    ).scalar()

    success_rate = 0.0

    if attempted:
        success_rate = round(
            (solved / attempted) * 100,
            2
        )

    return {
        "attempted": attempted,
        "solved": solved,
        "submissions": submissions,
        "success_rate": success_rate
    }


def get_topic_progress(user_id: int, db: Session):

    topics = db.query(Topic).all()

    result = []

    for topic in topics:

        attempted = db.query(
            func.count(func.distinct(UserProblemProgress.problem_id))
        ).join(
            ProblemTopic,
            ProblemTopic.problem_id == UserProblemProgress.problem_id
        ).filter(
            UserProblemProgress.user_id == user_id,
            ProblemTopic.topic_id == topic.id
        ).scalar()

        solved = db.query(
            func.count(func.distinct(UserProblemProgress.problem_id))
        ).join(
            ProblemTopic,
            ProblemTopic.problem_id == UserProblemProgress.problem_id
        ).filter(
            UserProblemProgress.user_id == user_id,
            UserProblemProgress.status == "solved",
            ProblemTopic.topic_id == topic.id
        ).scalar()

        success_rate = 0.0

        if attempted:
            success_rate = round(
                (solved / attempted) * 100,
                2
            )

        result.append({
            "topic_id": topic.id,
            "topic": topic.name,
            "attempted": attempted,
            "solved": solved,
            "success_rate": success_rate
        })

    return result


def get_weak_topics(user_id: int, db: Session):

    topics = get_topic_progress(user_id, db)

    weak_topics = [
        topic
        for topic in topics
        if topic["attempted"] >= 3
        and topic["success_rate"] < 60
    ]

    weak_topics.sort(
        key=lambda x: x["success_rate"]
    )

    return weak_topics

