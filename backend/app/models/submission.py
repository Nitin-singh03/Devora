from datetime import datetime

from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Submission(Base):
    __tablename__ = "submissions"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    problem_id: Mapped[int] = mapped_column(
        ForeignKey("problems.id"),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    language: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    runtime: Mapped[int | None] = mapped_column(
        nullable=True
    )

    memory: Mapped[int | None] = mapped_column(
        nullable=True
    )

    submitted_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    source: Mapped[str] = mapped_column(
        String(50),
        default="manual",
        nullable=False
    )