import uuid

from fastapi import HTTPException
from sqlalchemy import and_, or_, select

from src.dependencies.deps import SessionDep
from src.models import Meeting, MeetingParticipant
from src.schemas.meeting import MeetingCreateSchema


async def create_meeting(data: MeetingCreateSchema, session: SessionDep):
    stmt = (
        select(Meeting)
        .join(MeetingParticipant)
        .where(
            MeetingParticipant.user_id.in_(data.participant_ids),
            or_(
                and_(
                    Meeting.start_time <= data.start_time,
                    Meeting.end_time > data.start_time,
                ),
                and_(
                    Meeting.start_time < data.end_time,
                    Meeting.end_time >= data.end_time,
                ),
                and_(
                    Meeting.start_time >= data.start_time,
                    Meeting.end_time <= data.end_time,
                ),
            ),
        )
    )
    result = await session.execute(stmt)
    if result.scalars().first():
        raise HTTPException(
            status_code=400, detail="Time conflict with another meeting"
        )

    meeting = Meeting(
        title=data.title, start_time=data.start_time, end_time=data.end_time
    )
    session.add(meeting)
    await session.flush()

    for user_id in data.participant_ids:
        print(user_id, type(user_id))
        session.add(MeetingParticipant(meeting_id=meeting.id, user_id=user_id))

    await session.commit()
    await session.refresh(meeting)
    return meeting


async def list_user_meetings(user_id: uuid.UUID, session: SessionDep):
    stmt = (
        select(Meeting)
        .join(MeetingParticipant)
        .where(MeetingParticipant.user_id == user_id)
    )
    result = await session.execute(stmt)
    return result.scalars().all()


async def cancel_meeting(meeting_id: int, session: SessionDep):
    stmt = select(Meeting).where(Meeting.id == meeting_id)
    result = await session.execute(stmt)
    meeting = result.scalar_one_or_none()

    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    await session.delete(meeting)
    await session.commit()
