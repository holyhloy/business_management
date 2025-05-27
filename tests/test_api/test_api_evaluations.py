from datetime import date, timedelta

import pytest

from src.models import Evaluation
from src.models.task import Task, TaskStatus


@pytest.mark.asyncio
async def test_rate_task_success(
    session,
    client,
    completed_task,
    mock_user,
    override_current_user,
    override_require_role_admin,
):
    response = await client.post(
        "/evaluations/", json={"task_id": str(completed_task.id), "score": 4}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["task_id"] == completed_task.id
    assert data["user_id"] == str(mock_user.id)
    assert data["score"] == 4


@pytest.mark.asyncio
async def test_rate_task_task_not_found(
    client,
    override_current_user,
    override_require_role_admin,
):
    response = await client.post("/evaluations/", json={"task_id": 1, "score": 3})
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


@pytest.mark.asyncio
async def test_my_scores(
    client, session, mock_user, completed_task, override_current_user
):
    evaluation = Evaluation(
        task_id=completed_task.id,
        user_id=mock_user.id,
        score=5,
    )
    session.add(evaluation)
    await session.commit()

    response = await client.get("/evaluations/my")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["user_id"] == str(mock_user.id)
    assert data[0]["score"] == 5


@pytest.mark.asyncio
async def test_average_score(
    client, session, mock_user, completed_task, override_current_user
):
    today = date.today()
    evals = [
        Evaluation(
            task_id=completed_task.id, user_id=mock_user.id, score=3, created_at=today
        ),
    ]
    session.add_all(evals)
    await session.commit()

    response = await client.get(f"/evaluations/average?start={today}&end={today}")

    assert response.status_code == 200
    data = response.json()
    assert data["average_score"] == 3.0


@pytest.mark.asyncio
async def test_average_score_invalid_range(client, override_current_user):
    today = date.today()
    response = await client.get(
        f"/evaluations/average?start={today + timedelta(days=1)}&end={today}"
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Start time must be less or equal to end time"
