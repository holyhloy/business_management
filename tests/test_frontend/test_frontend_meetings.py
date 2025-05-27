import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_meetings_authenticated(
    client: AsyncClient,
    override_current_user_optional,
):
    response = await client.get("/meetings", follow_redirects=True)
    assert response.status_code == 200
    assert "Мои встречи" in response.text


@pytest.mark.asyncio
async def test_get_meetings_unauthenticated(client: AsyncClient):
    response = await client.get("/meetings", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/auth"
