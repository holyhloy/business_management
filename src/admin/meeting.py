import uuid

from wtforms import SelectMultipleField
from wtforms.validators import DataRequired

from src.admin.base import BaseAdmin
from src.models import MeetingParticipant, User
from src.models.meeting import Meeting
from sqlalchemy import select, or_, and_, delete


class MeetingAdmin(BaseAdmin, model=Meeting):
    column_list = [
        Meeting.id,
        Meeting.title,
        Meeting.start_time,
        Meeting.end_time,
    ]
    column_sortable_list = [Meeting.start_time]
    form_excluded_columns = [Meeting.participants]
    name_plural = "Встречи"

    async def scaffold_form(self, rules=None):
        form_class = await super().scaffold_form()
        async with self.session_maker() as session:
            users = (await session.execute(select(User))).scalars().all()
        form_class.participants = SelectMultipleField(
            "Участники",
            choices=[(str(u.id), u.email) for u in users],
            validators=[DataRequired()],
        )
        return form_class

    async def check_time_conflicts(
        self, start_time, end_time, participant_ids, exclude_meeting_id=None
    ):
        if start_time >= end_time:
            raise ValueError("Дата начала должна быть раньше даты окончания.")

        stmt = (
            select(Meeting)
            .join(MeetingParticipant)
            .where(
                MeetingParticipant.user_id.in_(participant_ids),
                or_(
                    and_(
                        Meeting.start_time <= start_time,
                        Meeting.end_time > start_time,
                    ),
                    and_(
                        Meeting.start_time < end_time,
                        Meeting.end_time >= end_time,
                    ),
                    and_(
                        Meeting.start_time >= start_time,
                        Meeting.end_time <= end_time,
                    ),
                ),
            )
        )
        if exclude_meeting_id:
            stmt = stmt.where(Meeting.id != exclude_meeting_id)

        async with self.session_maker() as session:
            result = await session.execute(stmt)
            if result.scalars().first():
                raise ValueError(
                    "Время встречи конфликтует с другой встречей участника."
                )

    async def insert_model(self, request, data):
        participants = data.pop("participants", [])
        participant_ids = [uuid.UUID(p) for p in participants]

        await self.check_time_conflicts(
            data["start_time"], data["end_time"], participant_ids
        )

        meeting = await super().insert_model(request, data)

        async with self.session_maker() as session:
            session.add_all(
                [
                    MeetingParticipant(meeting_id=meeting.id, user_id=pid)
                    for pid in participant_ids
                ]
            )
            await session.commit()

        return meeting

    async def update_model(self, request, pk, data):
        participants = data.pop("participants", [])
        participant_ids = [uuid.UUID(p) for p in participants]

        await self.check_time_conflicts(
            data["start_time"],
            data["end_time"],
            participant_ids,
            exclude_meeting_id=int(pk),
        )

        meeting = await super().update_model(request, pk, data)

        async with self.session_maker() as session:
            await session.execute(
                delete(MeetingParticipant).where(
                    MeetingParticipant.meeting_id == meeting.id
                )
            )
            session.add_all(
                [
                    MeetingParticipant(meeting_id=meeting.id, user_id=pid)
                    for pid in participant_ids
                ]
            )
            await session.commit()

        return meeting
