from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CommentCreateSchema(BaseModel):
    task_id: int
    content: str


class CommentReadSchema(BaseModel):
    id: int
    task_id: int
    user_id: UUID
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
