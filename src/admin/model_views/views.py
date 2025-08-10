from sqladmin import ModelView

from src.admin.forms import UserCreateForm
from src.db.models.models import UserOrm


class UserAdmin(ModelView, model=UserOrm):
    column_list = [UserOrm.id, UserOrm.username, UserOrm.email, UserOrm.is_superuser]

    form = UserCreateForm

    name = "Пользователь"
    name_plural = "Пользователи"
