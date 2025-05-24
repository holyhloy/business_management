from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from src.auth.auth import fastapi_users
from src.dependencies.deps import SessionDep
from src.models import User
from src.services.user_service import get_all_users

router = APIRouter()
current_user_optional = fastapi_users.current_user(optional=True)
templates = Jinja2Templates(directory="src/static")


def render_template(
    template_name: str, request: Request, context: dict
) -> HTMLResponse:
    if not context:
        context = {}
    user = getattr(request.state, "user", None)
    context.update({"request": request, "user": user})
    return templates.TemplateResponse(template_name, context)


@router.get("/")
async def root():
    return RedirectResponse(url="/auth")


@router.get("/auth", response_class=HTMLResponse)
async def redirect_auth(request: Request, user: User = Depends(current_user_optional)):
    if user is not None:
        return RedirectResponse(url="/index")
    return render_template("auth.html", request, {})


@router.get("/employees", response_class=HTMLResponse)
async def users(request: Request, user: User = Depends(current_user_optional)):
    if not user:
        return RedirectResponse(url="/auth")
    return render_template("users.html", request, {})


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
