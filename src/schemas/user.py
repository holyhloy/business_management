from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str


class UserReadSchema(BaseModel):
    id: UUID
    email: EmailStr
    role: str
    team_id: Optional[int]

    class Config:
        orm_mode = True


class UserUpdateSchema(BaseModel):
    email: Optional[EmailStr] = None
    role: Optional[str] = None
