from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.modules.dsa.problems.models import Platform, Problem
from app.modules.dsa.problems.schemas import (
    PlatformCreate,
    PlatformResponse,
    ProblemCreate,
    ProblemResponse,
)


router = APIRouter(
    prefix="/api/platforms",
    tags=["Platforms"]
)


@router.post(
    "",
    response_model=PlatformResponse,
    status_code=status.HTTP_201_CREATED
)
def create_platform(
    data: PlatformCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(Platform).filter(
        Platform.name == data.name
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Platform already exists"
        )

    platform = Platform(
        name=data.name
    )

    db.add(platform)
    db.commit()
    db.refresh(platform)

    return platform


@router.get(
    "",
    response_model=list[PlatformResponse]
)
def get_platforms(
    db: Session = Depends(get_db)
):
    return db.query(Platform).order_by(
        Platform.id
    ).all()


@router.post(
    "/problems",
    response_model=ProblemResponse,
    status_code=status.HTTP_201_CREATED
)
def create_problem(
    data: ProblemCreate,
    db: Session = Depends(get_db)
):
    platform = db.query(Platform).filter(
        Platform.id == data.platform_id
    ).first()

    if not platform:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Platform not found"
        )

    existing = db.query(Problem).filter(
        Problem.platform_id == data.platform_id,
        Problem.external_id == data.external_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Problem already exists on this platform"
        )

    problem = Problem(
        platform_id=data.platform_id,
        external_id=data.external_id,
        title=data.title,
        url=data.url,
        difficulty=data.difficulty,
        rating=data.rating
    )

    db.add(problem)
    db.commit()
    db.refresh(problem)

    return problem


@router.get(
    "/problems",
    response_model=list[ProblemResponse]
)
def get_problems(
    db: Session = Depends(get_db)
):
    return db.query(Problem).order_by(
        Problem.id
    ).all()
