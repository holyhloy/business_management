from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CommentCreateSchema(BaseModel):
    task_id: int
    content: str


class CommentReadSchema(BaseModel):
    id: int
    task_id: int
    user_id: UUID
    content: str
    created_at: datetime

    class Config:
        orm_mode = True
