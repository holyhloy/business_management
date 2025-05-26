from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse

from src.frontend.root import current_user_optional, render_template
from src.models import User

router = APIRouter()


@router.get("/auth", response_class=HTMLResponse)
async def redirect_auth(request: Request, user: User = Depends(current_user_optional)):
    if user is not None:
        return RedirectResponse(url="/index")
    return render_template("auth.html", request, {})
