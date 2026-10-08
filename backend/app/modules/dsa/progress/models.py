from datetime import datetime

from sqlalchemy import String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class UserProblemProgress(Base):
    __tablename__ = "user_problem_progress"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "problem_id",
            name="uq_user_problem_progress"
        ),
    )

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
        String(30),
        default="attempted",
        nullable=False
    )

    attempts: Mapped[int] = mapped_column(
        default=0,
        nullable=False
    )

    last_status: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    last_attempted_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    first_solved_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    last_solved_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
