from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.modules.users.models import User
from app.modules.auth.schemas import (
    SignupRequest,
    SignupResponse,
    LoginRequest,
    LoginResponse,
    ForgotPasswordRequest,
    ForgotPasswordResponse
)
from app.modules.auth.service import (
    register_user,
    authenticate_user,
    refresh_user_tokens,
    create_password_reset_otp
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


@router.post(
    "/forgot-password",
    response_model=ForgotPasswordResponse
)
def forgot_password(
    data: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == data.email
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    otp = create_password_reset_otp(
        user.id,
        db
    )

    return {
        "message": f"OTP generated successfully: {otp}"
    }