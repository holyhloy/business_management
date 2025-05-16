import logging
import uuid

from fastapi import Depends
from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from src.api.deps import SessionDep
from src.auth.config import SECRET
from src.db.session import Session
from src.models.user import User

logger = logging.getLogger("app")


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request=None):
        logger.info(f"User registered: {user.id}")


async def get_user_db():
    yield SQLAlchemyUserDatabase(Session(), User)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
