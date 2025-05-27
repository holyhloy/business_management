from uuid import uuid4

import pytest
import pytest_asyncio
from fastapi.requests import Request
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from src.core.config import settings
from src.db.session import get_session
from src.frontend.root import current_user_optional
from src.main import app
from src.models import *
from src.models.base import Base
from src.models.user import RoleEnum


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        follow_redirects=False,
    ) as client:
        yield client


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
    app.dependency_overrides[get_session] = override_get_session
    yield
    app.dependency_overrides.pop(get_session, None)


@pytest_asyncio.fixture
async def mock_user(session):
    user = User(
        id=uuid4(),
        email="eval_user@example.com",
        hashed_password="pwd",
        role=RoleEnum.EMPLOYEE,
    )
    session.add(user)
    await session.commit()
    return user


@pytest.fixture
def override_current_user_optional(mock_user):
    async def _override(request: Request):
        request.state.user = mock_user
        return mock_user

    app.dependency_overrides[current_user_optional] = _override
    yield
    app.dependency_overrides.pop(current_user_optional, None)


@pytest.fixture
def override_current_user_optional_none():
    async def _override():
        return None

    app.dependency_overrides[current_user_optional] = _override
    yield
    app.dependency_overrides.pop(current_user_optional, None)


@pytest_asyncio.fixture
async def users(session):
    user1 = User(email="user1@example.com", hashed_password="hashed1")
    user2 = User(email="user2@example.com", hashed_password="hashed2")
    session.add_all([user1, user2])
    await session.commit()
    return [user1, user2]
