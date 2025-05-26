import datetime

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse

from src.dependencies.deps import SessionDep
from src.frontend.root import current_user_optional, render_template
from src.services.calendar_service import get_calendar_days, get_calendar_view

router = APIRouter()


@router.get("/calendar", response_class=HTMLResponse)
async def get_frontend_calendar(
    request: Request,
    session: SessionDep,
    user=Depends(current_user_optional),
    target_date: datetime.date = datetime.date.today(),
    view_mode: str = "month",
):
    if not user:
        return RedirectResponse(url="/auth")

    calendar_data = await get_calendar_view(user.id, target_date, session)
    calendar_days = get_calendar_days(target_date)

    first_day = target_date.replace(day=1)
    prev_month = (first_day - datetime.timedelta(days=1)).replace(day=1)
    next_month = (first_day.replace(day=28) + datetime.timedelta(days=4)).replace(day=1)

    return render_template(
        "calendar.html",
        request,
        {
            "target_date": target_date,
            "days": calendar_days,
            "items_by_date": calendar_data,
            "view_mode": view_mode,
            "current_date": datetime.date.today(),
            "prev_month": prev_month,
            "next_month": next_month,
        },
    )
