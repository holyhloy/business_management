from datetime import date

from pydantic import BaseModel, ConfigDict

from src.schemas.meeting import MeetingReadSchema
from src.schemas.task import TaskReadSchema


# TODO: возможно, убрать
class CalendarDay(BaseModel):
    date: date
    tasks: list[TaskReadSchema]
    meetings: list[MeetingReadSchema]

    model_config = ConfigDict(from_attributes=True)
