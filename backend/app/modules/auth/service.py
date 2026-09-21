from sqlalchemy.orm import Session

from app.modules.users.models import User
from app.modules.auth.schemas import SignupRequest
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_refresh_token
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
