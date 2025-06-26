from fastapi_users.authentication import CookieTransport, JWTStrategy

from src.core.config import settings

SECRET = settings.SECRET_KEY

cookie_transport = CookieTransport(
    cookie_name="bizauth",
    cookie_max_age=3600,
)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)
