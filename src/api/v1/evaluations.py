from datetime import date

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from src.auth.auth import current_user
from src.core.cache_config import cache_key_builder
from src.dependencies.deps import SessionDep, require_role
from src.models.user import RoleEnum, User
from src.schemas.evaluation import EvaluationCreateSchema, EvaluationReadSchema
from src.schemas.user import UserReadSchema
from src.services.evaluation_service import (create_evaluation,
                                             get_average_score,
                                             get_user_evaluations)

router = APIRouter(prefix="/evaluations", tags=["Оценки задач"])


@router.post("/", response_model=EvaluationReadSchema)
async def rate_task(
    data: EvaluationCreateSchema,
    session: SessionDep,
    _: User = Depends(require_role(RoleEnum.ADMIN)),
):
    return await create_evaluation(data, session)


@router.get("/my", response_model=list[EvaluationReadSchema])
@cache(key_builder=cache_key_builder)
async def my_scores(
    session: SessionDep,
    user: UserReadSchema = Depends(current_user),
):
    return await get_user_evaluations(user.id, session)


@router.get("/average")
@cache(key_builder=cache_key_builder)
async def average_score(
    start: date,
    end: date,
    session: SessionDep,
    user: UserReadSchema = Depends(current_user),
):
    score = await get_average_score(user.id, start, end, session)
    return {"average_score": round(score, 2) if score else None}
