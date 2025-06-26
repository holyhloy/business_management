from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis
from src.core.cache_config import cache_key_builder
from src.core.config import settings
from src.db.init_db import create_db
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
