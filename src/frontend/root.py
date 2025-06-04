from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from src.auth.auth import fastapi_users

router = APIRouter()
current_user_optional = fastapi_users.current_user(optional=True)
templates = Jinja2Templates(directory="src/static")


def render_template(
    template_name: str, request: Request, context: dict = None
) -> HTMLResponse:
    if not context:
        context = {}
    user = getattr(request.state, "user", None)
    context.update({"user": user})
    return templates.TemplateResponse(request, template_name, context)


@router.get("/")
async def root():
    return RedirectResponse(url="/auth")
