from fastapi import APIRouter

from src.auth.auth import auth_backend, fastapi_users
from src.models.user import User
from src.schemas.user import UserCreateSchema, UserReadSchema, UserUpdateSchema

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserReadSchema, UserCreateSchema),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_users_router(UserReadSchema, UserUpdateSchema),
    prefix="/users",
    tags=["users"],
)
