from datetime import datetime, timedelta
from uuid import uuid4

import pytest
from sqlalchemy import select

from src.models import Meeting, MeetingParticipant, User


@pytest.mark.asyncio
async def test_create_meeting_success(
    session, client, override_require_role_admin, mock_user, override_current_user
):
    now = datetime.now()
    data = {
        "title": "Demo",
        "start_time": (now + timedelta(hours=1)).isoformat(),
        "end_time": (now + timedelta(hours=2)).isoformat(),
        "participant_ids": [str(mock_user.id)],
    }

    response = await client.post("/meetings/", json=data)

    assert response.status_code == 200
    resp = response.json()
    assert resp["title"] == "Demo"
    assert resp["participants"][0]["user"]["id"] == str(mock_user.id)


@pytest.mark.asyncio
async def test_create_meeting_conflict(
    session, client, override_require_role_admin, mock_user, override_current_user
):
    now = datetime.now()

    from src.models import Meeting, MeetingParticipant

    meeting = Meeting(
        title="Busy",
        start_time=now + timedelta(hours=1),
        end_time=now + timedelta(hours=2),
    )
    session.add(meeting)
    await session.flush()
    session.add(MeetingParticipant(meeting_id=meeting.id, user_id=mock_user.id))
    await session.commit()

    data = {
        "title": "New",
        "start_time": (now + timedelta(hours=1, minutes=30)).isoformat(),
        "end_time": (now + timedelta(hours=2, minutes=30)).isoformat(),
        "participant_ids": [str(mock_user.id)],
    }

    response = await client.post("/meetings/", json=data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Time conflict with another meeting"


@pytest.mark.asyncio
async def test_get_user_meetings(session, client, mock_user, override_current_user):
    now = datetime.now()

    meeting = Meeting(
        title="UserMeeting",
        start_time=now + timedelta(hours=2),
        end_time=now + timedelta(hours=3),
    )
    session.add(meeting)
    await session.flush()

    session.add(MeetingParticipant(meeting_id=meeting.id, user_id=mock_user.id))
    await session.commit()

    response = await client.get("/meetings/my")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert any(m["title"] == "UserMeeting" for m in data)


@pytest.mark.asyncio
async def test_cancel_meeting_success(session, client):
    now = datetime.now()
    meeting = Meeting(
        title="ToCancel",
        start_time=now + timedelta(hours=1),
        end_time=now + timedelta(hours=2),
    )
    session.add(meeting)
    await session.commit()

    response = await client.delete(f"/meetings/{meeting.id}")
    assert response.status_code == 204

    result = await session.execute(select(Meeting).where(Meeting.id == meeting.id))
    assert result.scalar_one_or_none() is None


@pytest.mark.asyncio
async def test_cancel_meeting_not_found(client):
    response = await client.delete("/meetings/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Meeting not found"
