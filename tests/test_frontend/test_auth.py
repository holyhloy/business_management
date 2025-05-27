import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_redirect_auth_authenticated(
    client: AsyncClient, override_current_user_optional
):
    response = await client.get("/auth", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/index"


@pytest.mark.asyncio
async def test_redirect_auth_unauthenticated(
    client: AsyncClient, override_current_user_optional_none
):
    response = await client.get("/auth")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
