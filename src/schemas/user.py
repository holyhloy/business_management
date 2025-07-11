import uuid
from typing import Optional

from fastapi_users import schemas


class UserCreateSchema(schemas.BaseUserCreate):
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserReadSchema(schemas.BaseUser[uuid.UUID]):
    id: uuid.UUID
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: str
    team_id: Optional[int] = None


class UserReadShortSchema(schemas.BaseUser[uuid.UUID]):
    id: uuid.UUID
    first_name: Optional[str]
    last_name: Optional[str]
    email: str


class UserUpdateSchema(schemas.BaseUserUpdate):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = None
