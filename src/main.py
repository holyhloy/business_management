from logging.config import dictConfig

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.admin.views import setup_admin
from src.api.v1 import main_router
from src.core.lisespan import lifespan
from src.core.logging_config import LOGGING_CONFIG
from src.frontend import frontend_router
from src.middleware.auth_context import InjectUserMiddleware
from src.models import *

dictConfig(LOGGING_CONFIG)

app = FastAPI(title="Business management system", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(InjectUserMiddleware)

app.include_router(main_router)
app.include_router(frontend_router)

setup_admin(app)
