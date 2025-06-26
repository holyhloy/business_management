from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


def render_template(
    template_name: str, request: Request, context: dict = None
) -> HTMLResponse:
    if not context:
        context = {}
    user = getattr(request.state, "user", None)
    context.update({"user": user})
    return templates.TemplateResponse(request, template_name, context)


templates = Jinja2Templates(directory="src/static")
