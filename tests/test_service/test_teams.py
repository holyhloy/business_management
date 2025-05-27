from uuid import UUID

import pytest
from fastapi import HTTPException

from src.models import User
from src.models.team import Team
from src.schemas.team import TeamCreateSchema, TeamUpdateSchema
from src.services.team_service import (create_team, delete_team, get_team,
                                       update_team)


@pytest.mark.asyncio
async def test_create_team(session):
    data = TeamCreateSchema(name="Team A", code="A001", users=[])
    team = await create_team(session, data)

    assert team.id is not None
    assert team.name == "Team A"
    assert team.code == "A001"


@pytest.mark.asyncio
async def test_get_team_existing(session):
    data = TeamCreateSchema(name="Team B", code="B001", users=[])
    created = await create_team(session, data)

    fetched = await get_team(session, created.id)
    assert fetched.id == created.id
    assert fetched.name == "Team B"


@pytest.mark.asyncio
async def test_get_team_not_found_raises(session):
    with pytest.raises(HTTPException) as exc_info:
        await get_team(session, team_id=9999)
    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_update_team(session):
    user = User(
        id=UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"),
        email="test@test.com",
        first_name="TEST",
        last_name="USER",
        hashed_password="fakehashed",
        is_active=True,
        is_verified=False,
        is_superuser=False,
        role="employee",
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    team = Team(name="Team C", code="C001", users=[user])
    session.add(team)
    await session.commit()
    await session.refresh(team)

    update_data = TeamUpdateSchema(name="Team C Updated", code="C002", users=[])
    updated = await update_team(session, team.id, update_data)

    assert updated.id == team.id
    assert updated.name == "Team C Updated"
    assert updated.code == "C002"
    assert updated.users == []


@pytest.mark.asyncio
async def test_update_team_conflict_raises(session):
    team1 = await create_team(
        session, TeamCreateSchema(name="Team D1", code="D001", users=[])
    )
    team2 = await create_team(
        session, TeamCreateSchema(name="Team D2", code="D002", users=[])
    )

    update_data = TeamUpdateSchema(name="Team D2 Updated", code="D001")
    with pytest.raises(HTTPException) as exc_info:
        await update_team(session, team2.id, update_data)
    assert exc_info.value.status_code == 409


@pytest.mark.asyncio
async def test_delete_team(session):
    team = await create_team(
        session, TeamCreateSchema(name="Team E", code="E001", users=[])
    )

    result = await delete_team(session, team.id)
    assert result is True

    with pytest.raises(HTTPException):
        await get_team(session, team.id)
