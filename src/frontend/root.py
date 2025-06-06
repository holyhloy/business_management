from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

from src.auth.auth import current_user_optional
from src.models import User

router = APIRouter()


@router.get("/")
async def root(user: User = Depends(current_user_optional)):
    if not user:
        return RedirectResponse(url="/auth", status_code=302)
    return RedirectResponse(url="/index", status_code=302)
