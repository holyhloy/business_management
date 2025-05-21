# services/evaluation_service.py
import datetime
from datetime import date
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import and_, func, select

from src.dependencies.deps import SessionDep
from src.models import Task
from src.models.evaluation import Evaluation
from src.models.task import TaskStatus
from src.schemas.evaluation import EvaluationCreateSchema


async def create_evaluation(
    data: EvaluationCreateSchema, session: SessionDep
) -> Evaluation:

    result = await session.execute(select(Task).where(Task.id == data.task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if not task.assignee_id:
        raise HTTPException(status_code=400, detail="Task has no assignee")

    if task.status != TaskStatus.completed:
        raise HTTPException(
            status_code=400, detail="Only completed tasks can be evaluated"
        )

    if task.evaluation:
        raise HTTPException(
            status_code=400, detail="This task already has an evaluation"
        )

    evaluation = Evaluation(
        task_id=data.task_id, user_id=task.assignee_id, score=data.score.value
    )

    session.add(evaluation)
    await session.commit()
    await session.refresh(evaluation)
    return evaluation


async def get_user_evaluations(user_id: UUID, session: SessionDep):
    result = await session.execute(
        select(Evaluation).where(Evaluation.user_id == user_id)
    )
    return result.scalars().all()


async def get_average_score(
    user_id: UUID, start: date, end: date, session: SessionDep
) -> float | None:
    if start > end:
        raise HTTPException(
            status_code=400, detail="Start time must be less or equal to end time"
        )
    if (
        start.year > datetime.datetime.now().year
        or end.year > datetime.datetime.now().year
    ):
        raise HTTPException(
            status_code=400, detail=f"It's {datetime.datetime.now().year} now"
        )

    result = await session.execute(
        select(func.avg(Evaluation.score)).where(
            and_(
                Evaluation.user_id == user_id,
                Evaluation.created_at >= start,
                Evaluation.created_at <= end,
            )
        )
    )
    return result.scalar()
