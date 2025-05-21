from fastapi import APIRouter, Depends

from src.auth.auth import current_user
from src.dependencies.deps import SessionDep, require_role
from src.models import User
from src.models.user import RoleEnum
from src.schemas.meeting import MeetingCreateSchema, MeetingReadSchema
from src.schemas.user import UserReadSchema
from src.services.meeting_service import (cancel_meeting, create_meeting,
                                          list_user_meetings)

router = APIRouter(prefix="/meetings", tags=["Встречи"])


@router.post("/", response_model=MeetingReadSchema)
async def create_meeting_endpoint(
    data: MeetingCreateSchema,
    session: SessionDep,
    _: User = Depends(require_role(RoleEnum.ADMIN)),
):
    print(data)
    return await create_meeting(data, session)


@router.get("/", response_model=list[MeetingReadSchema])
async def get_user_meetings(
    session: SessionDep,
    user: UserReadSchema = Depends(current_user),
):
    return await list_user_meetings(user.id, session)


@router.delete("/{meeting_id}", status_code=204)
async def cancel_meeting_endpoint(meeting_id: int, session: SessionDep):
    await cancel_meeting(meeting_id, session)
