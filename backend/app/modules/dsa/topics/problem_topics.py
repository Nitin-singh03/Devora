from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class ProblemTopic(Base):
    __tablename__ = "problem_topics"

    problem_id: Mapped[int] = mapped_column(
        ForeignKey("problems.id"),
        primary_key=True
    )

    topic_id: Mapped[int] = mapped_column(
        ForeignKey("topics.id"),
        primary_key=True
    )
