from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.modules.auth.schemas import (
    SignupRequest,
    SignupResponse,
    LoginRequest,
    LoginResponse
)
from app.modules.auth.service import (
    register_user,
    authenticate_user,
    refresh_user_tokens
)

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post(
    "/signup",
    response_model=SignupResponse,
    status_code=status.HTTP_201_CREATED
)
def signup(
    data: SignupRequest,
    db: Session = Depends(get_db)
):
    return register_user(db, data)


@router.post(
    "/login",
    response_model=LoginResponse
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):
    return authenticate_user(db, data.email, data.password)


@router.post(
    "/refresh",
    response_model=LoginResponse
)
def refresh_token(
    refresh_token: str
):
    return refresh_user_tokens(refresh_token)
