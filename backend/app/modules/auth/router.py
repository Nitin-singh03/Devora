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
    ForgotPasswordResponse,
    VerifyOTPRequest,
    VerifyOTPResponse,
    ResetPasswordRequest,
    ResetPasswordResponse
)
from app.modules.auth.service import (
    register_user,
    authenticate_user,
    refresh_user_tokens,
    create_password_reset_otp,
    verify_password_reset_otp,
    reset_password
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

    otp = create_password_reset_otp(
        user.id,
        db
    )

    return {
        "message": "If the email is registered, an OTP has been sent."
    }


@router.post(
    "/verify-otp",
    response_model=VerifyOTPResponse
)
def verify_otp(
    data: VerifyOTPRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == data.email
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP"
        )

    success, message = verify_password_reset_otp(
        user.id,
        data.otp,
        db
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )

    return {
        "message": "OTP verified successfully"
    }


@router.post(
    "/reset-password",
    response_model=ResetPasswordResponse
)
def reset_password_endpoint(
    data: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == data.email
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid request"
        )

    success, message = reset_password(
        user.id,
        data.otp,
        data.new_password,
        db
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )

    return {
        "message": message
    }