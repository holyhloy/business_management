from contextlib import asynccontextmanager
from logging.config import dictConfig
from typing import Any, AsyncGenerator

from fastapi import FastAPI
from sqladmin import Admin

from src.admin.evaluation import EvaluationAdmin
from src.admin.meeting import MeetingAdmin, MeetingParticipantAdmin
from src.admin.task import TaskAdmin, TaskCommentAdmin
from src.admin.team import TeamAdmin
from src.admin.user import UserAdmin
from src.api.v1 import main_router
from src.core.logging_config import LOGGING_CONFIG
from src.db.init_db import create_db
from src.db.session import engine
from src.models import *

dictConfig(LOGGING_CONFIG)

app = FastAPI(title="Business management system")
app.include_router(main_router)

admin = Admin(app, engine)

admin.add_view(UserAdmin)
admin.add_view(TeamAdmin)
admin.add_view(TaskAdmin)
admin.add_view(TaskCommentAdmin)
admin.add_view(EvaluationAdmin)
admin.add_view(MeetingAdmin)
admin.add_view(MeetingParticipantAdmin)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[Any, Any | None]:
    """
    Function provides Postgres and Redis pulling before
    app is started

    :param _: does nothing, using just to put it
    into lifespan param of app initialization

    :return: AsyncGenerator[Any | None]
    """
    await create_db()
    yield
