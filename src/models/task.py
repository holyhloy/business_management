import enum
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.evaluation import Evaluation
    from src.models.team import Team
    from src.models.user import User


class TaskStatus(str, enum.Enum):
    open = "open"
    in_progress = "in_progress"
    completed = "completed"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    deadline: Mapped[Optional[datetime]]
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus), default=TaskStatus.open
    )

    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    assignee_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))

    team: Mapped["Team"] = relationship(back_populates="tasks")
    assignee: Mapped["User"] = relationship(back_populates="tasks")
    comments: Mapped[List["TaskComment"]] = relationship(
        back_populates="task", cascade="all, delete"
    )
    evaluation: Mapped[Optional["Evaluation"]] = relationship(
        back_populates="task", uselist=False
    )


class TaskComment(Base):
    __tablename__ = "task_comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    task: Mapped[Task] = relationship(back_populates="comments")
    user: Mapped["User"] = relationship()
