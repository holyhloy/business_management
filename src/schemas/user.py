import uuid
from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreateSchema(schemas.BaseUserCreate):
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserReadSchema(schemas.BaseUser[uuid.UUID]):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: str
    team_id: Optional[int] = None


class UserUpdateSchema(schemas.BaseUserUpdate):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = None
