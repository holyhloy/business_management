from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, ConfigDict

class UserCreateSchema(BaseModel):
    first_name: str = None
    last_name: str = None
    email: EmailStr
    password: str


class UserReadSchema(BaseModel):
    id: UUID
    first_name: str = None
    last_name: str = None
    email: EmailStr
    role: str
    team_id: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class UserUpdateSchema(BaseModel):
    first_name: str = None
    last_name: str = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
