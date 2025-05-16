from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class MeetingBaseSchema(BaseModel):
    title: str
    start_time: datetime
    end_time: datetime


class MeetingCreateSchema(MeetingBaseSchema):
    participant_ids: List[UUID]


class MeetingReadSchema(MeetingBaseSchema):
    id: int
    participants: List[UUID]

    model_config = ConfigDict(from_attributes=True)
