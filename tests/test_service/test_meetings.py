import datetime

import pytest
import pytest_asyncio

from src.models.user import User
from src.schemas.meeting import MeetingCreateSchema
from src.services.meeting_service import (cancel_meeting, create_meeting,
                                          list_user_meetings)


@pytest_asyncio.fixture
async def users(session):
    u1 = User(email="u1@example.com", hashed_password="h1")
    u2 = User(email="u2@example.com", hashed_password="h2")
    session.add_all([u1, u2])
    await session.commit()
    return [u1, u2]


@pytest_asyncio.fixture
def meeting_data(users):
    now = datetime.datetime.now()
    return MeetingCreateSchema(
        title="Test Meeting",
        start_time=now + datetime.timedelta(hours=1),
        end_time=now + datetime.timedelta(hours=2),
        participant_ids=[users[0].id, users[1].id],
    )


@pytest.mark.asyncio
async def test_create_meeting(session, meeting_data):
    meeting = await create_meeting(meeting_data, session)

    assert meeting.id is not None
    assert meeting.title == "Test Meeting"
    assert len(meeting.participants) == 2


@pytest.mark.asyncio
async def test_create_conflicting_meeting_raises(session, meeting_data):
    await create_meeting(meeting_data, session)

    conflict_data = MeetingCreateSchema(
        title="Conflict",
        start_time=meeting_data.start_time + datetime.timedelta(minutes=30),
        end_time=meeting_data.end_time + datetime.timedelta(hours=1),
        participant_ids=meeting_data.participant_ids,
    )

    with pytest.raises(Exception) as e:
        await create_meeting(conflict_data, session)
    assert "Time conflict" in str(e.value)


@pytest.mark.asyncio
async def test_list_user_meetings(session, users, meeting_data):
    await create_meeting(meeting_data, session)

    meetings = await list_user_meetings(users[0].id, session)
    assert len(meetings) == 1
    assert meetings[0].title == "Test Meeting"


@pytest.mark.asyncio
async def test_cancel_meeting(session, meeting_data):
    meeting = await create_meeting(meeting_data, session)

    await cancel_meeting(meeting.id, session)

    meetings = await list_user_meetings(meeting_data.participant_ids[0], session)
    assert not meetings


@pytest.mark.asyncio
async def test_cancel_nonexistent_meeting(session):
    with pytest.raises(Exception) as e:
        await cancel_meeting(999999, session)
    assert "Meeting not found" in str(e.value)
