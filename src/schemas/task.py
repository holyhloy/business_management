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


class TaskUpdateSchema(TaskCreateSchema):
    pass


class TaskReadSchema(TaskBaseSchema):
    id: int
    team_id: int
    assignee_id: UUID

    model_config = ConfigDict(from_attributes=True)
