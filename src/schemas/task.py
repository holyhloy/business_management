from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TaskStatus(str, Enum):
    open = "open"
    in_progress = "in progress"
    completed = "completed"


class TaskBaseSchema(BaseModel):
    title: str
    description: str
    deadline: Optional[datetime]
    status: TaskStatus = TaskStatus.open


class TaskCreateSchema(TaskBaseSchema):
    team_id: int
    assignee_id: UUID


class TaskUpdateSchema(TaskCreateSchema):
    pass


class TaskReadSchema(TaskBaseSchema):
    id: int
    team_id: int
    assignee_id: UUID

    model_config = ConfigDict(from_attributes=True)
