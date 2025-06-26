import enum
import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.task import Task
    from src.models.user import User


class ScoreEnum(int, enum.Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


class Evaluation(Base):
    __tablename__ = "evaluations"

    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id", ondelete="cascade"), unique=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    score: Mapped[int] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())

    task: Mapped["Task"] = relationship(back_populates="evaluation", lazy="selectin")
    user: Mapped["User"] = relationship(back_populates="evaluations")

    def __repr__(self):
        return str(self.score)
