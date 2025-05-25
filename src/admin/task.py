from wtforms import IntegerField, SelectMultipleField, SelectField
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from wtforms.validators import DataRequired

from src.admin.base import BaseAdmin
from src.dependencies.deps import SessionDep
from src.models import Evaluation
from src.models.evaluation import ScoreEnum
from src.models.task import Task, TaskStatus
from fastapi.requests import Request


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

    async def scaffold_form(self, rules=None):
        print(rules, "Scaffold")
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
        print("insert")
        del data["evaluation_score"]
        task = await super().insert_model(request, data)
        return task

    async def update_model(self, request, pk, data):
        print("update")
        score = data.pop("evaluation_score", None)
        pk = int(pk)
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
