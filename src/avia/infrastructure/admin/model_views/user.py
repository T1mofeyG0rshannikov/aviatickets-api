from sqladmin import ModelView

from avia.infrastructure.admin.forms import UserCreateForm
from avia.infrastructure.persistence.db.models.models import UserOrm


class UserAdmin(ModelView, model=UserOrm):  # type: ignore
    column_list = [
        UserOrm.id,
        UserOrm.first_name,
        UserOrm.second_name,
        UserOrm.email,
        UserOrm.is_superuser,
    ]

    form = UserCreateForm

    name = "Пользователь"
    name_plural = "Пользователи"
