from sqlalchemy.orm import Session
import secrets
from datetime import datetime, timedelta
from app.modules.users.models import User
from app.modules.auth.models import PasswordResetOTP
from app.modules.auth.schemas import SignupRequest

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
    pwd_context
)
from app.shared.exceptions import ConflictException, UnauthorizedException


def register_user(db: Session, data: SignupRequest) -> User:
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise ConflictException(detail="Email already registered")

    user = User(
        name=data.name,
        email=data.email,
        password_hash=hash_password(data.password),
        auth_provider="local"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> dict:
    user = db.query(User).filter(User.email == email).first()
    if not user or not user.password_hash:
        raise UnauthorizedException(detail="Invalid email or password")

    if not verify_password(password, user.password_hash):
        raise UnauthorizedException(detail="Invalid email or password")

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


def refresh_user_tokens(refresh_token: str) -> dict:
    try:
        user_id = verify_refresh_token(refresh_token)
    except Exception:
        raise UnauthorizedException(detail="Invalid or expired refresh token")

    access_token = create_access_token(user_id)
    new_refresh_token = create_refresh_token(user_id)

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }

def generate_otp() -> str:
    return f"{secrets.randbelow(1_000_000):06d}"

def hash_otp(otp: str) -> str:
    return pwd_context.hash(otp)

def verify_otp(otp: str, otp_hash: str) -> bool:
    return pwd_context.verify(otp, otp_hash)

def create_password_reset_otp(user_id: int, db):
    db.query(PasswordResetOTP).filter(
        PasswordResetOTP.user_id == user_id,
        PasswordResetOTP.used == False
    ).update({
        PasswordResetOTP.used: True
    })
    otp = generate_otp()
    otp_hash = hash_otp(otp)

    expires_at = datetime.utcnow() + timedelta(minutes=10)

    reset_otp = PasswordResetOTP(
        user_id=user_id,
        otp_hash=otp_hash,
        expires_at=expires_at
    )

    db.add(reset_otp)
    db.commit()

    return otp

def verify_password_reset_otp(
    user_id: int,
    otp: str,
    db
):
    reset_otp = db.query(PasswordResetOTP).filter(
        PasswordResetOTP.user_id == user_id,
        PasswordResetOTP.used == False
    ).order_by(
        PasswordResetOTP.created_at.desc()
    ).first()

    if not reset_otp:
        return False, "OTP not found"

    if reset_otp.expires_at < datetime.utcnow():
        return False, "OTP expired"

    if reset_otp.attempts >= 5:
        return False, "Too many attempts"

    reset_otp.attempts += 1

    if not verify_otp(otp, reset_otp.otp_hash):
        db.commit()
        return False, "Invalid OTP"

    reset_otp.used = True
    db.commit()

    return True, "OTP verified"

def reset_password(
    user_id: int,
    otp: str,
    new_password: str,
    db
):
    reset_otp = db.query(PasswordResetOTP).filter(
        PasswordResetOTP.user_id == user_id,
        PasswordResetOTP.used == False
    ).order_by(
        PasswordResetOTP.created_at.desc()
    ).first()

    if not reset_otp:
        return False, "Invalid OTP"

    if reset_otp.expires_at < datetime.utcnow():
        return False, "OTP expired"

    if reset_otp.attempts >= 5:
        return False, "Too many attempts"

    if not verify_otp(otp, reset_otp.otp_hash):
        reset_otp.attempts += 1
        db.commit()
        return False, "Invalid OTP"

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        return False, "User not found"

    user.password_hash = pwd_context.hash(new_password)

    reset_otp.used = True

    db.commit()

    return True, "Password reset successfully"

def get_or_create_google_user(
    google_id: str,
    email: str,
    name: str,
    db
):
    user = db.query(User).filter(
        User.google_id == google_id
    ).first()

    if user:
        return user

    user = db.query(User).filter(
        User.email == email
    ).first()

    if user:
        user.google_id = google_id
        user.auth_provider = "google"

        db.commit()
        db.refresh(user)

        return user

    user = User(
        name=name,
        email=email,
        google_id=google_id,
        auth_provider="google"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def create_auth_tokens(user_id: int):
    return {
        "access_token": create_access_token(user_id),
        "refresh_token": create_refresh_token(user_id),
        "token_type": "bearer"
    }