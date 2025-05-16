import enum
import uuid

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class ScoreEnum(int, enum.Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


class Evaluation(Base):
    __tablename__ = "evaluations"

    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), unique=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    score: Mapped[ScoreEnum] = mapped_column(Enum(ScoreEnum))

    task: Mapped["Task"] = relationship(back_populates="evaluation")
    user: Mapped["User"] = relationship(back_populates="evaluations")
