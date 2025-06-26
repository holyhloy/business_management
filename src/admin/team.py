from src.admin.base import BaseAdmin
from src.models.team import Team


class TeamAdmin(BaseAdmin, model=Team):
    column_list = [Team.id, Team.name, Team.code, Team.users]
    column_searchable_list = [Team.name, Team.code]
    form_excluded_columns = ["tasks"]
    name_plural = "Команды"
    is_async = True
