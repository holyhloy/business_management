from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse

from src.auth.auth import current_user_optional
from src.frontend.config import render_template
from src.models import User

router = APIRouter()


@router.get("/profile", response_class=HTMLResponse)
async def profile(request: Request, user: User = Depends(current_user_optional)):
    if not user:
        return RedirectResponse(url="/auth")
    return render_template("profile.html", request, {})
