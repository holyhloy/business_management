import datetime

import pytest

from src.models import Evaluation
from src.models.task import Task
from src.models.user import User
from src.schemas.evaluation import EvaluationCreateSchema, ScoreEnum
from src.services.evaluation_service import (create_evaluation,
                                             get_average_score,
                                             get_user_evaluations)


@pytest.mark.asyncio
async def test_create_evaluation(session, completed_task):
    schema = EvaluationCreateSchema(task_id=completed_task.id, score=ScoreEnum.FOUR)
    evaluation = await create_evaluation(schema, session)

    assert evaluation.id is not None
    assert evaluation.task_id == completed_task.id
    assert evaluation.score == 4


@pytest.mark.asyncio
async def test_get_user_evaluations(session, completed_task):
    schema = EvaluationCreateSchema(task_id=completed_task.id, score=ScoreEnum.THREE)
    await create_evaluation(schema, session)

    evaluations = await get_user_evaluations(completed_task.assignee_id, session)
    assert len(evaluations) == 1
    assert evaluations[0].score == 3


@pytest.mark.asyncio
async def test_get_average_score(session, completed_task):
    await create_evaluation(
        EvaluationCreateSchema(task_id=completed_task.id, score=ScoreEnum.FIVE), session
    )

    today = datetime.date.today()
    avg = await get_average_score(
        completed_task.assignee_id,
        today.replace(day=1),
        today.replace(day=datetime.date.today().day + 1),
        session,
    )

    assert avg == 5.0


@pytest.mark.asyncio
async def test_get_average_score_invalid_dates(session, mock_user):
    start = datetime.date.today()
    end = start - datetime.timedelta(days=1)
    with pytest.raises(Exception) as e:
        await get_average_score(mock_user.id, start, end, session)
    assert "Start time must be less or equal" in str(e.value)


@pytest.mark.asyncio
async def test_get_average_score_future_year(session, mock_user):
    next_year = datetime.date.today().replace(year=datetime.date.today().year + 1)
    with pytest.raises(Exception) as e:
        await get_average_score(mock_user.id, next_year, next_year, session)
    assert "now" in str(e.value)
