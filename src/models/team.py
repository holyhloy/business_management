from typing import List, Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    code: Mapped[Optional[str]] = mapped_column(String(32), unique=True, nullable=True)

    users: Mapped[List["User"]] = relationship(back_populates="team")
    tasks: Mapped[List["Task"]] = relationship(back_populates="team")
