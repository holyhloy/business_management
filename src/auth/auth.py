import uuid

from fastapi import Request
from fastapi.responses import RedirectResponse, Response
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy,
)
from sqladmin.authentication import AuthenticationBackend as AdminBackend
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware

from src.auth.manager import UserManager, get_user_db, get_user_manager
from src.core.config import settings
from src.core.logging_config import logger
from src.models.user import RoleEnum, User

SECRET = settings.SECRET_KEY

cookie_transport = CookieTransport(
    cookie_name="bizauth",
    cookie_max_age=3600,
    cookie_samesite="none",
    cookie_secure=True,
)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()


class AdminAuth(AdminBackend):
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.middlewares = [
            Middleware(SessionMiddleware, secret_key=self.secret_key),
        ]

    async def login(self, request: Request) -> Response | bool:
        form = await request.form()
        email = form.get("username")
        password = form.get("password")

        try:
            user_db_gen = get_user_db()
            user_db = await anext(user_db_gen)
            user_manager = UserManager(user_db)
        except StopAsyncIteration as e:
            logger.info(f"Error while getting a value from user_db_gen agenerator: {e}")
            return False

        try:
            user = await user_manager.get_by_email(email)
            valid, _ = user_manager.password_helper.verify_and_update(
                password, user.hashed_password
            )

            if valid and user.role == RoleEnum.ADMIN:
                request.session["admin_user_id"] = str(user.id)
                logger.info(
                    f"User {user.id} has been logged in admin panel successfully"
                )
                return RedirectResponse(url="/admin", status_code=302)

        except Exception as e:
            logger.info(f"[AdminAuth] Login error: {e}")
        finally:
            await user_db_gen.aclose()

        return False

    async def logout(self, request: Request) -> RedirectResponse:
        user = request.session["admin_user_id"]
        request.session.clear()
        logger.info(f"User {user} has been logged out of admin panel successfully")
        return RedirectResponse(url="/admin/login", status_code=302)

    async def authenticate(self, request: Request) -> bool | Response:
        path = str(request.url.path)

        if path.startswith("/admin/login") or path.startswith("/admin/logout"):
            return True

        user_id = request.session.get("admin_user_id")
        if not user_id:
            return False

        try:
            user_db_gen = get_user_db()
            user_db = await anext(user_db_gen)
            user_manager = UserManager(user_db)
        except StopAsyncIteration as e:
            logger.info(f"Error while getting a value from user_db_gen agenerator: {e}")
            return False

        try:
            user = await user_manager.get(uuid.UUID(user_id))
            return user.role == RoleEnum.ADMIN
        except Exception as e:
            logger.info(f"[AdminAuth] Auth error: {e}")
            return False
        finally:
            await user_db_gen.aclose()


admin_auth_backend = AdminAuth(SECRET)
