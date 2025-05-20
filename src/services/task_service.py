from uuid import UUID

from sqlalchemy import delete, select, update

from src.api.deps import SessionDep
from src.core.logging_config import logger
from src.models.task import Task
from src.schemas.task import TaskCreateSchema, TaskUpdateSchema


async def create_task(session: SessionDep, data: TaskCreateSchema) -> Task:
    task = Task(**data.model_dump())
    session.add(task)
    await session.commit()
    await session.refresh(task)
    logger.info(f"Task {data.title} created")
    return task


async def get_task(session: SessionDep, task_id: int) -> Task | None:
    result = await session.execute(select(Task).where(Task.id == task_id))
    return result.scalar_one_or_none()


async def list_tasks(session: SessionDep, assignee_id: UUID) -> list[Task]:
    result = await session.execute(select(Task).where(Task.assignee_id == assignee_id))
    return result.scalars().all()


async def update_task(
    session: SessionDep, task_id: int, data: TaskUpdateSchema
) -> Task | None:
    stmt = (
        update(Task)
        .where(Task.id == task_id)
        .values(**data.model_dump(exclude_unset=True))
        .returning(Task)
    )
    result = await session.execute(stmt)
    task = result.scalar_one_or_none()
    await session.commit()
    return task


async def delete_task(session: SessionDep, task_id: int) -> bool:
    stmt = delete(Task).where(Task.id == task_id)
    await session.execute(stmt)
    await session.commit()
    return True
