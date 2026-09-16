from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Problem(Base):
    __tablename__ = "problems"

    id: Mapped[int] = mapped_column(primary_key=True)

    platform_id: Mapped[int] = mapped_column(
        ForeignKey("platforms.id"),
        nullable=False
    )

    external_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    url: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    difficulty: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    rating: Mapped[int | None] = mapped_column(
        nullable=True
    )