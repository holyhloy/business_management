import uuid
from typing import Optional

from fastapi import Depends
from fastapi.requests import Request
from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users.exceptions import UserAlreadyExists
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.exc import IntegrityError

from src.auth.config import SECRET
from src.core.logging_config import logger
from src.db.session import Session
from src.models.user import RoleEnum, User
from src.schemas.user import UserCreateSchema, UserUpdateSchema


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def create(
        self,
        user_create: UserCreateSchema,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> User:
        await self.validate_password(user_create.password, user_create)

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        logger.info(f"Password for user {user_create.email} created")

        if user_dict.get("is_superuser"):
            user_dict["role"] = RoleEnum.ADMIN

        try:
            created_user = await self.user_db.create(user_dict)
            await self.on_after_register(created_user, request)
            return created_user
        except IntegrityError:
            logger.info(
                f"Attempt of creating user with existing email: {user_create.email}"
            )
            raise UserAlreadyExists()

    async def update(
        self,
        user_update: UserUpdateSchema,
        user: User,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> User:
        if safe:
            updated_user_data = user_update.create_update_dict()
        else:
            updated_user_data = user_update.create_update_dict_superuser()
            if updated_user_data.get("is_superuser"):
                updated_user_data["role"] = RoleEnum.ADMIN
        updated_user = await self._update(user, updated_user_data)
        await self.on_after_update(updated_user, updated_user_data, request)
        return updated_user

    async def on_after_register(self, user: User, request=None):
        logger.info(f"User registered: {user.id}")


async def get_user_db():
    async with Session() as session:
        yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
