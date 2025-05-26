from fastapi_users.password import PasswordHelper
from wtforms import PasswordField

from src.admin.base import BaseAdmin
from src.models.user import User


class UserAdmin(BaseAdmin, model=User):
    column_list = [
        User.email,
        User.first_name,
        User.last_name,
        User.role,
        User.team,
    ]
    column_labels = {
        User.email: "Email",
        User.first_name: "Имя",
        User.last_name: "Фамилия",
        User.role: "Должность",
        User.team: "Команда",
    }
    column_searchable_list = [User.email, User.first_name, User.last_name]
    column_sortable_list = [User.email, User.role]
    form_excluded_columns = [
        "id",
        "hashed_password",
        User.tasks,
        User.evaluations,
        User.meetings,
    ]

    form_overrides = {
        "password": PasswordField,
    }
    name_plural = "Пользователи"

    async def scaffold_form(self, rules):
        form_class = await super().scaffold_form()
        form_class.password = PasswordField("Пароль")  # добавляем обычное поле пароля
        return form_class

    async def insert_model(self, request, data):
        password = data.pop("password", None)
        if password:
            data["hashed_password"] = PasswordHelper().hash(password)
        return await super().insert_model(request, data)

    async def update_model(self, request, pk, data):
        password = data.pop("password", None)
        if password:
            data["hashed_password"] = PasswordHelper().hash(password)
        return await super().update_model(request, pk, data)
