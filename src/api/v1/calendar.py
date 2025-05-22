from datetime import date

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from src.auth.auth import current_user
from src.core.cache_config import cache_key_builder
from src.dependencies.deps import SessionDep
from src.schemas.calendar import CalendarDay
from src.schemas.user import UserReadSchema
from src.services.calendar_service import get_calendar_view

router = APIRouter()


@router.get("/calendar")
@cache(key_builder=cache_key_builder)
async def calendar_view(
    target_date: date,
    session: SessionDep,
    user: UserReadSchema = Depends(current_user),
):
    return await get_calendar_view(user.id, target_date, session)
