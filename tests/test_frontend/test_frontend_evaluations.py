import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_front_evaluations_authenticated(
    client: AsyncClient,
    override_current_user_optional,
):
    response = await client.get("/evaluations", follow_redirects=True)
    assert response.status_code == 200
    assert (
        "Оценки" in response.text or "evaluations" in response.text
    )


@pytest.mark.asyncio
async def test_get_front_evaluations_unauthenticated(client: AsyncClient):
    response = await client.get("/evaluations", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/auth"
