from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from src.core.config import settings

engine = create_async_engine(settings.DB_URL, pool_pre_ping=True)
Session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_session() -> AsyncGenerator[AsyncSession, Any]:
    """
    Yields session for manipulating with database data

    :return: session object
    """
    async with Session() as session:
        yield session
