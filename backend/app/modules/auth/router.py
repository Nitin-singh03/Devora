from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from app.core.oauth import oauth
from app.db.database import get_db
from app.core.security import create_access_token, create_refresh_token
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
    reset_password,
    get_or_create_google_user,
    create_auth_tokens
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


@router.get("/google/login")
async def google_login(request: Request):
    redirect_uri = request.url_for(
        "google_callback"
    )

    return await oauth.google.authorize_redirect(
        request,
        str(redirect_uri)
    )


@router.get("/google/callback")
async def google_callback(
    request: Request,
    db: Session = Depends(get_db)
):
    token = await oauth.google.authorize_access_token(
        request
    )

    user_info = token.get("userinfo")

    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to retrieve Google user"
        )

    user = get_or_create_google_user(
        google_id=user_info["sub"],
        email=user_info["email"],
        name=user_info.get(
            "name",
            user_info["email"].split("@")[0]
        ),
        db=db
    )

    return create_auth_tokens(user.id)