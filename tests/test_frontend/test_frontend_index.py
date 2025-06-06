import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_index_authenticated(
    client: AsyncClient,
    override_current_user_optional,
):
    response = await client.get("/index", follow_redirects=True)
    assert response.status_code == 200
    assert "Добро пожаловать" in response.text


@pytest.mark.asyncio
async def test_get_index_unauthenticated(client: AsyncClient):
    response = await client.get("/index", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["location"] == "/auth"
