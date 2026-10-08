from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.modules.dsa.problems.models import Problem
from app.modules.dsa.topics.models import Topic
from app.modules.dsa.topics.problem_topics import ProblemTopic
from app.modules.dsa.topics.schemas import (
    TopicCreate,
    TopicResponse
)
from app.modules.users.models import User


router = APIRouter(
    prefix="/api/topics",
    tags=["Topics"]
)


@router.post(
    "",
    response_model=TopicResponse,
    status_code=status.HTTP_201_CREATED
)
def create_topic(
    data: TopicCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing = db.query(Topic).filter(
        Topic.name == data.name
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Topic already exists"
        )

    topic = Topic(name=data.name)

    db.add(topic)
    db.commit()
    db.refresh(topic)

    return topic


@router.get(
    "",
    response_model=list[TopicResponse]
)
def get_topics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Topic).order_by(
        Topic.name
    ).all()


@router.post("/{topic_id}/problems/{problem_id}")
def assign_topic_to_problem(
    topic_id: int,
    problem_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    topic = db.query(Topic).filter(
        Topic.id == topic_id
    ).first()

    if not topic:
        raise HTTPException(
            status_code=404,
            detail="Topic not found"
        )

    problem = db.query(Problem).filter(
        Problem.id == problem_id
    ).first()

    if not problem:
        raise HTTPException(
            status_code=404,
            detail="Problem not found"
        )

    existing = db.query(ProblemTopic).filter(
        ProblemTopic.topic_id == topic_id,
        ProblemTopic.problem_id == problem_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Topic already assigned to problem"
        )

    relation = ProblemTopic(
        topic_id=topic_id,
        problem_id=problem_id
    )

    db.add(relation)
    db.commit()

    return {
        "message": "Topic assigned successfully"
    }
