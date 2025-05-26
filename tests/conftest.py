import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from src.core.config import settings
from src.db.session import get_session
from src.models import *
from src.models.base import Base


@pytest_asyncio.fixture()
async def session():
    engine_test = create_async_engine(settings.DB_URL, echo=False)
    async_session_factory = async_sessionmaker(
        engine_test, expire_on_commit=False, class_=AsyncSession
    )

    async with engine_test.begin() as conn:
        assert settings.MODE == "TEST"
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_factory() as session:
        yield session

    await engine_test.dispose()


@pytest.fixture()
def override_get_session(session):
    async def _override():
        yield session

    return _override


@pytest.fixture(autouse=True)
def set_test_session(override_get_session):
    from src.main import app

    app.dependency_overrides[get_session] = override_get_session
