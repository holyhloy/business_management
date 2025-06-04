import uuid
from calendar import monthrange
from collections import defaultdict
from datetime import date, timedelta
from typing import Any

from sqlalchemy import and_, select

from src.dependencies.deps import SessionDep
from src.models import Meeting, MeetingParticipant, Task


def get_calendar_days(target_date: date) -> list[date]:
    year, month = target_date.year, target_date.month
    first_day = date(year, month, 1)
    last_day = date(year, month, monthrange(year, month)[1])

    # Сдвигаем к началу недели (Пн = 0), чтобы календарь начинался с понедельника
    start_delta = first_day.weekday()  # Пн=0, Вс=6
    start_date = first_day - timedelta(days=start_delta)

    end_delta = 6 - last_day.weekday()
    end_date = last_day + timedelta(days=end_delta)

    total_days = (end_date - start_date).days + 1
    return [start_date + timedelta(days=i) for i in range(total_days)]


def get_next_month_start(current: date) -> date:
    if current.month == 12:
        return date(current.year + 1, 1, 1)
    return date(current.year, current.month + 1, 1)


async def get_calendar_view(
    user_id: uuid.UUID,
    target_date: date,
    session: SessionDep,
) -> dict[date, dict[str, list[Any]]]:

    if not isinstance(user_id, uuid.UUID):
        raise ValueError("Invalid user_id")

    start_of_month = target_date.replace(day=1)
    next_month = get_next_month_start(start_of_month)

    tasks_query = await session.execute(
        select(Task).where(
            and_(
                Task.assignee_id == user_id,
                Task.deadline >= start_of_month,
                Task.deadline < next_month,
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

    calendar_data: dict[date, dict[str, list[Any]]] = defaultdict(
        lambda: {"tasks": [], "meetings": []}
    )

    for task in tasks:
        calendar_data[task.deadline.date()]["tasks"].append(task)

    for meeting in meetings:
        calendar_data[meeting.start_time.date()]["meetings"].append(meeting)

    return calendar_data
