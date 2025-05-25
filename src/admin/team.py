from src.admin.base import BaseAdmin
from src.models.team import Team


class TeamAdmin(BaseAdmin, model=Team):
    column_list = [Team.id, Team.name, Team.code]
    column_searchable_list = [Team.name, Team.code]
    form_excluded_columns = ["users", "tasks"]
    name_plural = "Команды"
