from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from src.core.cache_config import cache_key_builder
from src.dependencies.deps import require_role
from src.models.user import RoleEnum, User
from src.schemas.team import TeamReadSchema
from src.services.team_service import *

router = APIRouter(prefix="/teams", tags=["Команды"])


@router.post("/", response_model=TeamReadSchema)
async def create_team_endpoint(
    data: TeamCreateSchema,
    session: SessionDep,
    _: User = Depends(require_role(RoleEnum.ADMIN)),
):
    return await create_team(session, data)


@router.get("/{team_id}", response_model=TeamReadSchema)
async def get_team_endpoint(team_id: int, session: SessionDep):
    return await get_team(session, team_id)


@router.put("/{team_id}", response_model=TeamReadSchema)
async def update_team_endpoint(
    team_id: int,
    data: TeamUpdateSchema,
    session: SessionDep,
    _: User = Depends(require_role(RoleEnum.ADMIN)),
):
    return await update_team(session, team_id, data)


@router.delete("/{team_id}")
async def delete_team_endpoint(
    team_id: int, session: SessionDep, _: User = Depends(require_role(RoleEnum.ADMIN))
):
    await delete_team(session, team_id)
    return {"status": "deleted"}
