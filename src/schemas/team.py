from typing import Optional

from pydantic import BaseModel, ConfigDict

from src.schemas.user import UserReadShortSchema


class TeamBaseSchema(BaseModel):
    name: str
    code: Optional[str] = None


class TeamCreateSchema(TeamBaseSchema):
    users: Optional[list[UserReadShortSchema]] = None


class TeamUpdateSchema(TeamCreateSchema):
    name: Optional[str] = None
    code: Optional[str] = None


class TeamReadSchema(TeamCreateSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)
