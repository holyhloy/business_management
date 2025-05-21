from fastapi import HTTPException
from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError

from src.api.deps import SessionDep
from src.core.logging_config import logger
from src.models.team import Team
from src.schemas.team import TeamCreateSchema, TeamUpdateSchema


async def create_team(session: SessionDep, data: TeamCreateSchema) -> Team:
    team = Team(**data.model_dump())
    session.add(team)
    await session.commit()
    await session.refresh(team)
    logger.info(f"Team {data.name} created")
    return team


async def get_team(session: SessionDep, team_id: int) -> Team | None:
    result = await session.execute(select(Team).where(Team.id == team_id))
    team = result.scalar_one_or_none()
    if team:
        return team
    else:
        raise HTTPException(status_code=404, detail=f"Team with ID {team_id} not found")


async def update_team(
    session: SessionDep, team_id: int, data: TeamUpdateSchema
) -> Team | None:
    stmt = (
        update(Team)
        .where(Team.id == team_id)
        .values(**data.model_dump(exclude_unset=True))
        .returning(Team)
    )
    try:
        result = await session.execute(stmt)
    except IntegrityError:
        raise HTTPException(
            status_code=409, detail=f"Team with code {data.code} is already exists"
        )
    team = result.scalar_one_or_none()
    await session.commit()
    return team


async def delete_team(session: SessionDep, team_id: int) -> bool:
    stmt = delete(Team).where(Team.id == team_id)
    await session.execute(stmt)
    await session.commit()
    return True
