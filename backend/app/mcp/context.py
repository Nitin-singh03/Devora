from sqlalchemy.orm import Session

from app.db.database import SessionLocal


class MCPContext:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.db: Session = SessionLocal()

    def close(self):
        self.db.close()
