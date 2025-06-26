from datetime import datetime
from typing import Self
from uuid import UUID

from pydantic import BaseModel, ConfigDict, model_validator

from src.schemas.user import UserReadShortSchema


class MeetingBaseSchema(BaseModel):
    title: str
    start_time: datetime
    end_time: datetime

    @model_validator(mode="after")
    def check_dates(self) -> Self:
        if self.start_time > self.end_time:
            raise ValueError("Start time must be less than end time")
        return self


class MeetingParticipantReadSchema(BaseModel):
    user: UserReadShortSchema


class MeetingCreateSchema(MeetingBaseSchema):
    participant_ids: list[UUID]


class MeetingReadSchema(MeetingBaseSchema):
    id: int
    participants: list[MeetingParticipantReadSchema]

    model_config = ConfigDict(from_attributes=True)
