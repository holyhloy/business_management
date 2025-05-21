import enum
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ScoreEnum(int, enum.Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


class EvaluationCreateSchema(BaseModel):
    task_id: int
    score: ScoreEnum


class EvaluationReadSchema(BaseModel):
    id: int
    task_id: int
    user_id: UUID
    score: ScoreEnum
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
