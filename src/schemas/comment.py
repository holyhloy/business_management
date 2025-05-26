from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CommentBaseSchema(BaseModel):
    task_id: int
    content: str
    created_at: datetime


class CommentCreateSchema(BaseModel):
    content: str


class CommentReadSchema(CommentBaseSchema):
    id: int
    user_id: UUID

    model_config = ConfigDict(from_attributes=True)
