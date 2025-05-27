import pytest

from tests.conftest import mock_user


@pytest.mark.asyncio
async def test_create_team(
    session, client, override_require_role_admin, override_current_user, mock_user
):
    data = {"name": "Test", "code": "TST123", "users": []}

    response = await client.post("/teams/", json=data)
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == data["name"]
    assert body["code"] == data["code"]


@pytest.mark.asyncio
async def test_get_team(
    session, client, override_require_role_admin, override_current_user
):
    data = {"name": "Team A", "code": "CODEA", "users": []}
    created = await client.post("/teams/", json=data)
    team_id = created.json()["id"]

    response = await client.get(f"/teams/{team_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Team A"


@pytest.mark.asyncio
async def test_update_team(
    session, client, override_require_role_admin, override_current_user
):
    data = {"name": "Old Name", "code": "OLD123", "users": []}
    created = await client.post("/teams/", json=data)
    team_id = created.json()["id"]

    updated_data = {"name": "New Name"}

    updated = await client.put(f"/teams/{team_id}", json=updated_data)
    assert updated.status_code == 200
    assert updated.json()["name"] == "New Name"
    assert updated.json()["code"] == "OLD123"  # code не изменяли


@pytest.mark.asyncio
async def test_delete_team(
    session, client, override_require_role_admin, override_current_user
):
    data = {"name": "Delete Me", "code": "DEL123", "users": []}
    created = await client.post("/teams/", json=data)
    team_id = created.json()["id"]

    deleted = await client.delete(f"/teams/{team_id}")
    assert deleted.status_code == 200
    assert deleted.json()["status"] == "deleted"

    after = await client.get(f"/teams/{team_id}")
    assert after.status_code == 404
