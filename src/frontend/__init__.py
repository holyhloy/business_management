from fastapi import APIRouter

from src.frontend.auth import router as auth_router
from src.frontend.calendar import router as calendar_router
from src.frontend.evaluations import router as evaluations_router
from src.frontend.index import router as index_router
from src.frontend.meetings import router as meetings_router
from src.frontend.profile import router as profile_router
from src.frontend.root import router as root_router
from src.frontend.tasks import router as tasks_router

frontend_router = APIRouter(tags=["Frontend routes"])
frontend_router.include_router(root_router)
frontend_router.include_router(auth_router)
frontend_router.include_router(calendar_router)
frontend_router.include_router(evaluations_router)
frontend_router.include_router(index_router)
frontend_router.include_router(meetings_router)
frontend_router.include_router(profile_router)
frontend_router.include_router(tasks_router)
