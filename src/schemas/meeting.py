from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.schemas.user import UserReadShortSchema


class MeetingBaseSchema(BaseModel):
    title: str
    start_time: datetime
    end_time: datetime


class MeetingParticipantReadSchema(BaseModel):
    user: UserReadShortSchema


class MeetingCreateSchema(MeetingBaseSchema):
    participant_ids: list[UUID]


class MeetingReadSchema(MeetingBaseSchema):
    id: int
    participants: list[MeetingParticipantReadSchema]

    model_config = ConfigDict(from_attributes=True)
