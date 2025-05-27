from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.models.task import TaskStatus


class TaskBaseSchema(BaseModel):
    title: str
    description: str
    deadline: Optional[datetime]
    status: TaskStatus = TaskStatus.open


class TaskCreateSchema(TaskBaseSchema):
    team_id: Optional[int]
    assignee_id: UUID


class TaskUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    status: Optional[TaskStatus] = None
    team_id: Optional[int] = None
    assignee_id: Optional[UUID] = None


class TaskReadSchema(TaskBaseSchema):
    id: int
    team_id: int
    assignee_id: UUID

    model_config = ConfigDict(from_attributes=True)
