from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse

from src.auth.auth import current_user_optional
from src.dependencies.deps import SessionDep
from src.frontend.config import render_template
from src.models import User
from src.services.task_service import list_tasks
from src.services.user_service import get_all_users

router = APIRouter()


@router.get("/tasks", response_class=HTMLResponse)
async def get_frontend_my_tasks(
    request: Request, session: SessionDep, user: User = Depends(current_user_optional)
):
    if not user:
        return RedirectResponse(url="/auth")
    user_list = await get_all_users(session)
    tasks_list = await list_tasks(session, user.id)
    return render_template(
        "tasks.html", request, {"users": user_list, "tasks": tasks_list}
    )
