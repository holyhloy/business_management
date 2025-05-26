from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from src.auth.auth import current_user
from src.core.cache_config import cache_key_builder
from src.dependencies.deps import require_role
from src.models.user import RoleEnum, User
from src.schemas.comment import CommentReadSchema
from src.schemas.task import TaskReadSchema
from src.schemas.user import UserReadSchema
from src.services.task_service import *

router = APIRouter(prefix="/tasks", tags=["Задачи"])


@router.post("/", response_model=TaskReadSchema)
async def create_task_endpoint(
    data: TaskCreateSchema,
    session: SessionDep,
    _: User = Depends(require_role(RoleEnum.ADMIN)),
):
    return await create_task(session, data)


@router.get("/{task_id}", response_model=TaskReadSchema)
@cache(key_builder=cache_key_builder)
async def get_task_endpoint(task_id: int, session: SessionDep):
    return await get_task(session, task_id)


@router.put("/{task_id}", response_model=TaskReadSchema)
async def update_task_endpoint(
    task_id: int,
    data: TaskUpdateSchema,
    session: SessionDep,
    _: User = Depends(require_role(RoleEnum.ADMIN)),
):
    return await update_task(session, task_id, data)


@router.delete("/{task_id}")
async def delete_task_endpoint(
    task_id: int, session: SessionDep, _: User = Depends(require_role(RoleEnum.ADMIN))
):
    await delete_task(session, task_id)
    return {"status": "deleted"}


@router.post("/{task_id}/comments", response_model=CommentReadSchema)
async def add_comment(
    task_id: int,
    comment: CommentCreateSchema,
    session: SessionDep,
    user: UserReadSchema = Depends(current_user),
):
    return await add_comment_to_task(session, task_id, user.id, comment)


@router.get("/{task_id}/comments", response_model=list[CommentReadSchema])
@cache(key_builder=cache_key_builder)
async def get_comments(
    task_id: int,
    session: SessionDep,
    _: UserReadSchema = Depends(current_user),
):
    return await get_comments_for_task(session, task_id)
