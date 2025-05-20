from src.admin.base import BaseAdmin
from src.models.evaluation import Evaluation


class EvaluationAdmin(BaseAdmin, model=Evaluation):
    column_list = [
        Evaluation.id,
        Evaluation.task_id,
        Evaluation.user_id,
        Evaluation.score,
    ]
    column_sortable_list = [Evaluation.score]
