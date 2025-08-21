from sqladmin import ModelView

from src.infrastructure.admin.forms import UserCreateForm
from src.infrastructure.db.models.models import UserOrm


class UserAdmin(ModelView, model=UserOrm):
    column_list = [
        UserOrm.id,
        UserOrm.first_name,
        UserOrm.second_name,
        UserOrm.email,
        UserOrm.is_superuser,
        UserOrm.hash_password,
    ]

    form = UserCreateForm

    name = "Пользователь"
    name_plural = "Пользователи"
