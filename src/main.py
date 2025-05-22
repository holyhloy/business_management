from contextlib import asynccontextmanager
from logging.config import dictConfig
from typing import Any, AsyncGenerator

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin

from src.admin.evaluation import EvaluationAdmin
from src.admin.meeting import MeetingAdmin, MeetingParticipantAdmin
from src.admin.task import TaskAdmin, TaskCommentAdmin
from src.admin.team import TeamAdmin
from src.admin.user import UserAdmin
from src.api.v1 import main_router
from src.auth.auth import admin_auth_backend
from src.core.cache_config import cache_key_builder
from src.core.config import settings
from src.core.logging_config import LOGGING_CONFIG
from src.db.init_db import create_db
from src.db.session import engine
from src.models import *


async def clear_cache():
    await FastAPICache.clear()


scheduler = AsyncIOScheduler()
scheduler.add_job(clear_cache, "interval", seconds=60)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[Any, Any | None]:
    """
    Function provides Postgres and Redis pulling before
    app is started

    :param _: does nothing, using just to put it
    into lifespan param of app initialization

    :return: AsyncGenerator[Any | None]
    """
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}")
    FastAPICache.init(
        RedisBackend(redis), prefix="api:cache", key_builder=cache_key_builder
    )
    scheduler.start()
    await clear_cache()
    await create_db()
    yield


dictConfig(LOGGING_CONFIG)

app = FastAPI(title="Business management system", lifespan=lifespan)
app.include_router(main_router)

admin = Admin(app, engine, authentication_backend=admin_auth_backend)

admin.add_view(UserAdmin)
admin.add_view(TeamAdmin)
admin.add_view(TaskAdmin)
admin.add_view(TaskCommentAdmin)
admin.add_view(EvaluationAdmin)
admin.add_view(MeetingAdmin)
admin.add_view(MeetingParticipantAdmin)
