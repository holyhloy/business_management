from fastapi import HTTPException
from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError

from src.core.logging_config import logger
from src.dependencies.deps import SessionDep
from src.models import User
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
    update_data = data.model_dump(exclude_unset=True)

    users_data = update_data.pop("users", None)

    stmt = update(Team).where(Team.id == team_id).values(**update_data).returning(Team)
    try:
        result = await session.execute(stmt)
    except IntegrityError:
        raise HTTPException(
            status_code=409, detail=f"Team with code {data.code} already exists"
        )

    team = result.scalar_one_or_none()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    if users_data is not None:
        team.users.clear()
        for user_data in users_data:
            user_dict = (
                user_data.model_dump()
                if hasattr(user_data, "model_dump")
                else user_data
            )
            user = await session.get(User, user_dict.get("id"))
            if user is None:
                user = User(**user_dict)
                session.add(user)
            team.users.append(user)

    await session.commit()
    await session.refresh(team)
    return team


async def delete_team(session: SessionDep, team_id: int) -> bool:
    stmt = delete(Team).where(Team.id == team_id)
    await session.execute(stmt)
    await session.commit()
    logger.info(f"Team with ID {team_id} deleted")
    return True
