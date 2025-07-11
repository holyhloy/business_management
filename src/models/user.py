import enum
import uuid
from typing import TYPE_CHECKING, List, Optional

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.evaluation import Evaluation
    from src.models.meeting import MeetingParticipant
    from src.models.task import Task
    from src.models.team import Team


class RoleEnum(str, enum.Enum):
    EMPLOYEE = "employee"
    MANAGER = "manager"
    ADMIN = "admin"


class User(SQLAlchemyBaseUserTableUUID, Base):
    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    first_name: Mapped[str] = mapped_column(String(64), nullable=True)
    last_name: Mapped[str] = mapped_column(String(128), nullable=True)
    team_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("teams.id"), nullable=True
    )
    role: Mapped[RoleEnum] = mapped_column(default=RoleEnum.EMPLOYEE)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    team: Mapped[Optional["Team"]] = relationship(
        back_populates="users", lazy="selectin"
    )
    tasks: Mapped[List["Task"]] = relationship(
        back_populates="assignee", lazy="selectin"
    )
    evaluations: Mapped[List["Evaluation"]] = relationship(
        back_populates="user", cascade="all, delete"
    )
    meetings: Mapped[List["MeetingParticipant"]] = relationship(
        back_populates="user", lazy="selectin"
    )

    def __repr__(self):
        return f"ID: {self.id}, E-Mail: {self.email}, First Name: {self.first_name}"
