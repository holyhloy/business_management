from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.core.config import settings


engine = create_async_engine(settings.DB_URL, pool_pre_ping=True)
Session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
