from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse

from src.auth.auth import current_user_optional
from src.dependencies.deps import SessionDep
from src.frontend.config import render_template
from src.models import User
from src.services.user_service import get_all_users

router = APIRouter()


@router.get("/meetings", response_class=HTMLResponse)
async def get_frontend_meetings(
    request: Request, session: SessionDep, user: User = Depends(current_user_optional)
):
    if not user:
        return RedirectResponse(url="/auth", status_code=302)
    user_list = await get_all_users(session)
    return render_template("meetings.html", request, {"users": user_list})
