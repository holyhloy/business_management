from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends

from src.auth.auth import current_user
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
async def my_scores(
    session: SessionDep,
    user: UserReadSchema = Depends(current_user),
    _: User = Depends(require_role(RoleEnum.ADMIN)),
):
    return await get_user_evaluations(user.id, session)


@router.get("/average")
async def average_score(
    start: date,
    end: date,
    session: SessionDep,
    user: UserReadSchema = Depends(current_user),
):
    score = await get_average_score(user.id, start, end, session)
    return {"average_score": round(score, 2) if score else None}
