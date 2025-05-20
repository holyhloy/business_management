from fastapi import APIRouter

from src.api.v1.auth import router as auth_router

main_router = APIRouter()
main_router.include_router(auth_router)
