from wtforms import SelectField

from src.admin.base import BaseAdmin
from src.models import Evaluation, User
from src.models.task import Task


class TaskAdmin(BaseAdmin, model=Task):
    column_list = [
        Task.id,
        Task.title,
        Task.status,
        Task.deadline,
        Task.assignee,
        Task.team,
        Task.evaluation,
    ]
    column_sortable_list = [Task.id, Task.deadline, Task.status]
    column_searchable_list = [Task.title]
    column_filters = [Task.status]
    column_labels = {
        Task.id: "ID",
        Task.title: "Название",
        Task.status: "Статус",
        Task.deadline: "Дедлайн",
        Task.assignee: "Исполнитель",
        Task.team: "Команда",
        Task.evaluation: "Оценка",
    }
    form_excluded_columns = ["comments", Task.evaluation]
    name_plural = "Задачи"
    is_async = True

    async def scaffold_form(self, rules=None):
        form_class = await super().scaffold_form()
        choices = [(None, None)]
        choices.extend([(str(i), str(i)) for i in range(1, 6)])
        form_class.evaluation_score = SelectField(
            "Оценка",
            choices=choices,
            coerce=str,
            default=None,
        )
        return form_class

    async def insert_model(self, request, data):
        del data["evaluation_score"]
        team = data["team"]
        async with self.session_maker() as session:
            user = await session.get(User, data["assignee"])
        if team:
            if int(team) != user.team_id:
                raise ValueError(f"Пользователь относится к команде {user.team}")

        task = await super().insert_model(request, data)
        return task

    async def update_model(self, request, pk, data):
        score = data.pop("evaluation_score", None)
        pk = int(pk)
        team = data["team"]
        async with self.session_maker() as session:
            user = await session.get(User, data["assignee"])
        if team:
            if int(team) != user.team_id:
                raise ValueError(f"Пользователь относится к команде {user.team}")
        task = await super().update_model(request, pk, data)
        try:
            score = int(score)
        except ValueError:
            score = None
        if score:
            async with self.session_maker() as session:
                db_task = await session.get(Task, pk)
                if db_task.evaluation:
                    db_task.evaluation.score = score
                else:
                    if db_task.status == "completed":
                        db_task.evaluation = Evaluation(
                            task_id=pk,
                            user_id=db_task.assignee_id,
                            score=score,
                        )
                    else:
                        raise ValueError("Оценивать можно только завершенные задачи")
                await session.commit()
        return task
