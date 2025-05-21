import uuid
from collections import defaultdict
from datetime import date, datetime, timedelta
from typing import Any, Coroutine

from sqlalchemy import and_, select

from src.dependencies.deps import SessionDep
from src.models import Meeting, MeetingParticipant, Task


async def get_calendar_view(
    user_id: uuid.UUID,
    target_date: date,
    session: SessionDep,
) -> defaultdict[Any, dict[str, list[Any]]]:

    start_of_month = target_date.replace(day=1)
    if start_of_month.month == 12:
        next_month = start_of_month.replace(year=start_of_month.year + 1, month=1)
    else:
        next_month = start_of_month.replace(month=start_of_month.month + 1)

    tasks_query = await session.execute(
        select(Task).where(
            and_(
                Task.assignee_id == user_id,
                Task.deadline >= start_of_month,
                Task.deadline <= next_month,
            )
        )
    )
    tasks = tasks_query.scalars().all()

    meetings_query = await session.execute(
        select(Meeting)
        .join(Meeting.participants)
        .where(
            and_(
                MeetingParticipant.user_id == user_id,
                Meeting.start_time >= start_of_month,
                Meeting.start_time < next_month,
            )
        )
    )
    meetings = meetings_query.scalars().all()

    # Сборка по дням
    calendar = {}
    for t in tasks:
        d = t.deadline
        calendar.setdefault(d, {"tasks": [], "meetings": []})
        calendar[d]["tasks"].append(t)

    for m in meetings:
        d = m.start_time
        calendar.setdefault(d, {"tasks": [], "meetings": []})
        calendar[d]["meetings"].append(m)

    calendar_data = defaultdict(lambda: {"tasks": [], "meetings": []})

    for task in tasks:
        calendar_data[task.deadline.date()]["tasks"].append(task)

    for meeting in meetings:
        calendar_data[meeting.start_time.date()]["meetings"].append(meeting)

    return calendar_data
