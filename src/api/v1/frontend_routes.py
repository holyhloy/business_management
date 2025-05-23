from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from src.auth.auth import fastapi_users
from src.models import User

router = APIRouter()
current_user_optional = fastapi_users.current_user(optional=True)
templates = Jinja2Templates(directory="src/static")


def get_user(request):
    return getattr(request.state, "user", None)


templates.env.globals["user"] = get_user


@router.get("/")
async def root():
    return RedirectResponse(url="/auth")


@router.get("/auth", response_class=HTMLResponse)
async def redirect_auth(request: Request, user: User = Depends(current_user_optional)):
    if user is not None:
        return RedirectResponse(url="/index")
    return templates.TemplateResponse("auth.html", {"request": request})


@router.get("/employees", response_class=HTMLResponse)
async def users(request: Request, user: User = Depends(current_user_optional)):
    if not user:
        return RedirectResponse(url="/auth")
    return templates.TemplateResponse("users.html", {"request": request, "user": user})


@router.get("/index", response_class=HTMLResponse)
async def index(request: Request, user: User = Depends(current_user_optional)):
    if not user:
        return RedirectResponse(url="/auth")
    return templates.TemplateResponse("index.html", {"request": request, "user": user})


@router.get("/rates", response_class=HTMLResponse)
async def evaluations(request: Request, user: User = Depends(current_user_optional)):
    if not user:
        return RedirectResponse(url="/auth")
    return templates.TemplateResponse(
        "evaluations.html", {"request": request, "user": user}
    )


@router.get("/profile", response_class=HTMLResponse)
async def profile(request: Request, user: User = Depends(current_user_optional)):
    if not user:
        return RedirectResponse(url="/auth")
    return templates.TemplateResponse(
        "profile.html", {"request": request, "user": user}
    )
