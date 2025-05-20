from sqladmin import ModelView


class BaseAdmin(ModelView):
    page_size = 20
    can_export = True
    name_plural = "Records"
