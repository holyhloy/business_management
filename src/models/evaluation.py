from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base
import uuid

class Evaluation(Base):
    __tablename__ = 'evaluations'

    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey('tasks.id'), unique=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('user.id'))
    score: Mapped[int] = mapped_column()

    task: Mapped['Task'] = relationship(back_populates='evaluation')
    user: Mapped['User'] = relationship(back_populates='evaluations')
    