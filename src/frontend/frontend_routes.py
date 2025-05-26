import datetime

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from src.auth.auth import fastapi_users
from src.dependencies.deps import SessionDep
from src.frontend.root import current_user_optional, render_template
from src.models import User
from src.services.calendar_service import get_calendar_days, get_calendar_view
from src.services.task_service import list_tasks
from src.services.user_service import get_all_users

router = APIRouter()


@router.get("/auth", response_class=HTMLResponse)
async def redirect_auth(request: Request, user: User = Depends(current_user_optional)):
    if user is not None:
        return RedirectResponse(url="/index")
    return render_template("auth.html", request, {})


@router.get("/index", response_class=HTMLResponse)
async def index(request: Request, user: User = Depends(current_user_optional)):
    if not user:
        return RedirectResponse(url="/auth")
    return render_template("index.html", request, {})


@router.get("/rates", response_class=HTMLResponse)
async def evaluations(request: Request, user: User = Depends(current_user_optional)):
    if not user:
        return RedirectResponse(url="/auth")
    return render_template("evaluations.html", request, {})


@router.get("/profile", response_class=HTMLResponse)
async def profile(request: Request, user: User = Depends(current_user_optional)):
    if not user:
        return RedirectResponse(url="/auth")
    return render_template("profile.html", request, {})


@router.get("/meets", response_class=HTMLResponse)
async def meets(
    request: Request, session: SessionDep, user: User = Depends(current_user_optional)
):
    if not user:
        return RedirectResponse(url="/auth")
    user_list = await get_all_users(session)
    return render_template("meetings.html", request, {"users": user_list})


@router.get("/my_assignments", response_class=HTMLResponse)
async def my_assignments(
    request: Request, session: SessionDep, user: User = Depends(current_user_optional)
):
    if not user:
        return RedirectResponse(url="/auth")
    user_list = await get_all_users(session)
    tasks_list = await list_tasks(session, user.id)
    return render_template(
        "tasks.html", request, {"users": user_list, "tasks": tasks_list}
    )


@router.get("/schedule", response_class=HTMLResponse)
async def schedule(
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
