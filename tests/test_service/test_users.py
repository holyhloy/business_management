import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User
from src.services.user_service import get_all_users


@pytest.mark.asyncio
async def test_get_all_users_returns_users(session: AsyncSession):
    user1 = User(email="user1@example.com", hashed_password="hashed1")
    user2 = User(email="user2@example.com", hashed_password="hashed2")
    session.add_all([user1, user2])
    await session.commit()

    result = await get_all_users(session)

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0].email == "user1@example.com"


@pytest.mark.asyncio
async def test_get_all_users_empty_raises_404(session: AsyncSession):
    with pytest.raises(HTTPException) as exc_info:
        await get_all_users(session)

    assert exc_info.value.status_code == 404
    assert "Some error" in exc_info.value.detail
