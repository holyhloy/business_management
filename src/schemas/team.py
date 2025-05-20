from typing import Optional

from pydantic import BaseModel, ConfigDict


class TeamBaseSchema(BaseModel):
    name: str
    code: Optional[str] = None


class TeamCreateSchema(TeamBaseSchema):
    pass


class TeamReadSchema(TeamBaseSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)
