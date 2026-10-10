import os
from contextvars import ContextVar
from typing import Optional
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.mcp.auth import authenticate_mcp_token

_current_user_id: ContextVar[Optional[int]] = ContextVar("current_user_id", default=None)


def set_current_user_id(user_id: int):
    return _current_user_id.set(user_id)


def get_current_user_id() -> int:
    """
    Resolve authenticated user ID for the MCP session.
    1. Check async ContextVar (set by MCP session/middleware).
    2. Check DEVORA_ACCESS_TOKEN (JWT token passed by MCP client / environment).
    3. Check DEVORA_USER_ID environment variable (dev/test override).
    4. Fallback to 1 for local development.
    """
    user_id = _current_user_id.get()
    if user_id is not None:
        return user_id

    token = os.getenv("DEVORA_ACCESS_TOKEN")
    if token:
        try:
            return authenticate_mcp_token(token)
        except Exception:
            pass

    env_user_id = os.getenv("DEVORA_USER_ID")
    if env_user_id:
        try:
            return int(env_user_id)
        except ValueError:
            pass

    return 1


class MCPContext:
    def __init__(
        self,
        user_id: Optional[int] = None,
        db: Optional[Session] = None,
    ):
        self.user_id = user_id if user_id is not None else get_current_user_id()
        self._owns_db = db is None
        self.db: Session = db if db is not None else SessionLocal()

    def close(self):
        if self._owns_db and self.db:
            self.db.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

