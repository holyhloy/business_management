from fastapi import FastAPI
from sqladmin import Admin

from src.admin.meeting import MeetingAdmin
from src.admin.task import TaskAdmin
from src.admin.team import TeamAdmin
from src.admin.user import UserAdmin
from src.auth.auth import admin_auth_backend
from src.db.session import engine
from src.models import *


def setup_admin(app: FastAPI) -> None:
    admin = Admin(app, engine, authentication_backend=admin_auth_backend)
    admin.add_view(UserAdmin)
    admin.add_view(TeamAdmin)
    admin.add_view(TaskAdmin)
    admin.add_view(MeetingAdmin)
