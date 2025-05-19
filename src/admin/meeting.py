from src.admin.base import BaseAdmin
from src.models import MeetingParticipant
from src.models.meeting import Meeting


class MeetingAdmin(BaseAdmin, model=Meeting):
    column_list = [Meeting.id, Meeting.title, Meeting.start_time, Meeting.end_time]
    column_sortable_list = [Meeting.start_time]
    form_excluded_columns = ["participants"]


class MeetingParticipantAdmin(BaseAdmin, model=MeetingParticipant):
    column_list = [
        MeetingParticipant.id,
        MeetingParticipant.meeting_id,
        MeetingParticipant.user_id,
    ]
    column_sortable_list = [MeetingParticipant.meeting_id]
