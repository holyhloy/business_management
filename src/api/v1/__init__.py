from fastapi import APIRouter

from src.api.v1.auth import router as auth_router
from src.api.v1.evaluations import router as evals_router
from src.api.v1.tasks import router as tasks_router
from src.api.v1.teams import router as teams_router

main_router = APIRouter()
main_router.include_router(auth_router)
main_router.include_router(tasks_router)
main_router.include_router(teams_router)
main_router.include_router(evals_router)
