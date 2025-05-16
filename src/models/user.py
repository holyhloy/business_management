import uuid
from typing import List, Optional

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    first_name: Mapped[str]
    last_name: Mapped[str]
    team_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("teams.id"), nullable=True
    )
    role: Mapped[str] = mapped_column(default="employee")

    team: Mapped[Optional["Team"]] = relationship(back_populates="users")
    tasks: Mapped[List["Task"]] = relationship(back_populates="assignee")
    evaluations: Mapped[List["Evaluation"]] = relationship(back_populates="user")
    meetings: Mapped[List["MeetingParticipant"]] = relationship(back_populates="user")
