from sqlalchemy.orm import Session

from app.db.database import SessionLocal


class MCPContext:
    def __init__(
        self,
        user_id: int,
        db: Session
    ):
        self.user_id = user_id
        self.db = db
