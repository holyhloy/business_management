from typing import Optional

from pydantic import BaseModel


class TeamBaseSchema(BaseModel):
    name: str
    code: Optional[str] = None


class TeamCreateSchema(TeamBaseSchema):
    pass


class TeamReadSchema(TeamBaseSchema):
    id: int

    class Config:
        orm_mode = True
