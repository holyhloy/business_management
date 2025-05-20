from src.admin.base import BaseAdmin
from src.models.task import Task, TaskComment


class TaskAdmin(BaseAdmin, model=Task):
    column_list = [
        Task.id,
        Task.title,
        Task.description,
        Task.status,
        Task.deadline,
        Task.assignee_id,
        Task.team_id,
    ]
    column_searchable_list = [Task.title]
    column_sortable_list = [Task.id, Task.deadline, Task.status]
    form_excluded_columns = ["comments", "evaluation", "team", "assignee"]


class TaskCommentAdmin(BaseAdmin, model=TaskComment):
    column_list = [
        TaskComment.id,
        TaskComment.task_id,
        TaskComment.user_id,
        TaskComment.content,
        TaskComment.created_at,
    ]
    column_sortable_list = [TaskComment.created_at]
