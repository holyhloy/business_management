

from fastapi import APIRouter, Depends

from src.api.deps import SessionDep, require_role
from src.models.user import RoleEnum, User
from src.schemas.task import TaskCreateSchema, TaskReadSchema, TaskUpdateSchema
from src.services.task_service import *

router = APIRouter(prefix="/tasks", tags=["Задачи"])


@router.post("/", response_model=TaskReadSchema)
async def create_task_endpoint(
    data: TaskCreateSchema,
    session: SessionDep,
    _: User = Depends(require_role(RoleEnum.ADMIN)),
):
    return await create_task(session, data)


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
