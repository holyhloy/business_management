from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError

from src.core.logging_config import logger
from src.dependencies.deps import SessionDep
from src.models import TaskComment
from src.models.task import Task
from src.schemas.comment import CommentCreateSchema
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
    task = result.scalar_one_or_none()
    if task:
        return task
    else:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")


async def list_tasks(session: SessionDep, assignee_id: UUID) -> list[Task]:
    result = await session.execute(select(Task).where(Task.assignee_id == assignee_id))
    return result.scalars().all()


async def list_all_tasks(session: SessionDep) -> list[Task]:
    result = await session.execute(select(Task))
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


async def add_comment_to_task(
    session: SessionDep, task_id: int, user_id: UUID, comment_data: CommentCreateSchema
) -> TaskComment:
    comment = TaskComment(
        task_id=task_id,
        user_id=user_id,
        content=comment_data.content,
    )
    session.add(comment)
    try:
        await session.commit()
        await session.refresh(comment)
        logger.info(f"Comment {comment.id} for task {comment.task_id} created")
    except IntegrityError:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
    return comment


async def get_comments_for_task(session: SessionDep, task_id: int) -> list[TaskComment]:
    result = await session.execute(
        select(TaskComment)
        .where(TaskComment.task_id == task_id)
        .order_by(TaskComment.created_at)
    )
    return result.scalars().all()
