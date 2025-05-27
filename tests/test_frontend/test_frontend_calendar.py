import datetime

import pytest
from httpx import AsyncClient

from src.models import Meeting, MeetingParticipant, Task
from src.schemas.task import TaskStatus


@pytest.mark.asyncio
async def test_get_frontend_calendar_authenticated(
    client: AsyncClient,
    session,
    mock_user,
    override_current_user_optional,
):
    today = datetime.datetime.now()

    task = Task(
        title="Calendar Task",
        assignee_id=mock_user.id,
        deadline=today,
        status=TaskStatus.in_progress,
    )
    session.add(task)

    meeting = Meeting(
        title="Calendar Meeting",
        start_time=datetime.datetime(today.year, today.month, today.day, 10),
        end_time=datetime.datetime(today.year, today.month, today.day, 11),
    )
    session.add(meeting)
    await session.flush()

    session.add(MeetingParticipant(meeting_id=meeting.id, user_id=mock_user.id))
    await session.commit()

    response = await client.get("/calendar", follow_redirects=True)
    assert response.status_code == 200
    assert "Calendar Task" in response.text
    assert "Calendar Meeting" in response.text


@pytest.mark.asyncio
async def test_get_frontend_calendar_unauthenticated(client: AsyncClient):
    response = await client.get("/calendar", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/auth"
