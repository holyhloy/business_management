from typing import Optional

from fastapi import Depends
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.types import ASGIApp

from src.auth.auth import current_user
from src.models.user import User


class InjectUserMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, user_dependency=Depends(current_user)):
        super().__init__(app)
        self.user_dependency = user_dependency

    async def dispatch(self, request: Request, call_next):
        try:
            user: Optional[User] = await self.user_dependency(request)
        except Exception:
            user = None

        request.state.user = user
        response = await call_next(request)
        return response
