import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.user import User


class Meeting(Base):
    __tablename__ = "meetings"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    start_time: Mapped[datetime] = mapped_column(DateTime)
    end_time: Mapped[datetime] = mapped_column(DateTime)

    participants: Mapped[List["MeetingParticipant"]] = relationship(
        back_populates="meeting", cascade="all, delete", lazy="selectin", uselist=True
    )

    def __repr__(self):
        return self.title


class MeetingParticipant(Base):
    __tablename__ = "meeting_participants"

    id: Mapped[int] = mapped_column(primary_key=True)
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meetings.id"))
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))

    meeting: Mapped[Meeting] = relationship(
        back_populates="participants", lazy="selectin"
    )
    user: Mapped["User"] = relationship(back_populates="meetings", lazy="selectin")

    def __repr__(self):
        return self.user.email
