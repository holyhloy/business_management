import datetime

import pytest

from src.models import Meeting, MeetingParticipant, Task, User
from src.schemas.task import TaskStatus
from src.services.calendar_service import get_calendar_days, get_calendar_view


@pytest.mark.asyncio
async def test_get_calendar_view(session, mock_user):
    user_id = mock_user.id
    today = datetime.date.today()
    deadline = datetime.datetime.combine(today.replace(day=15), datetime.time(12))
    start = datetime.datetime.combine(today.replace(day=20), datetime.time(10))
    end = start + datetime.timedelta(hours=1)

    task = Task(
        title="Task",
        assignee_id=user_id,
        deadline=deadline,
        status=TaskStatus.open,
    )
    session.add(task)

    meeting = Meeting(
        title="Meeting",
        start_time=start,
        end_time=end,
    )
    session.add(meeting)
    await session.flush()

    session.add(MeetingParticipant(meeting_id=meeting.id, user_id=user_id))
    await session.commit()

    result = await get_calendar_view(user_id, today, session)

    assert deadline.date().isoformat() in result
    assert start.date().isoformat() in result

    assert task in result[deadline.date().isoformat()]["tasks"]
    assert meeting in result[start.date().isoformat()]["meetings"]


def test_get_calendar_days_range():
    date_input = datetime.date(2024, 4, 15)  # апрель 2024
    days = get_calendar_days(date_input)

    assert days[0].weekday() == 0  # понедельник
    assert days[-1].weekday() == 6  # воскресенье
    assert len(days) in [35, 42]  # 5–6 недель
    assert days[0] <= datetime.date(2024, 4, 1)
    assert days[-1] >= datetime.date(2024, 4, 30)
