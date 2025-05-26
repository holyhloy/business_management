import re

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from src.auth.auth import get_jwt_strategy
from src.auth.manager import UserManager, get_user_db
from src.core.logging_config import logger


class InjectUserMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.strategy = get_jwt_strategy()

    async def dispatch(self, request: Request, call_next):
        try:
            cookies = request.headers.get("cookie")
            match = re.search(r"bizauth=([^;]+)", cookies)
            token = match.group(1) if match else None

            user_db_gen = get_user_db()
            user_db = await anext(user_db_gen)
            user_manager = UserManager(user_db)
            user = await self.strategy.read_token(token, user_manager)
        except Exception as e:
            logger.info(f"InjectUserMiddleware: Unable to load user - {e}")
            user = None

        request.state.user = user
        response = await call_next(request)
        return response
