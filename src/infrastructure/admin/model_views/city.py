from src.infrastructure.admin.model_views.base import BaseModelView
from src.infrastructure.persistence.db.models.models import CityOrm


class CityAdmin(BaseModelView, model=CityOrm):  # type: ignore
    column_list = [CityOrm.id, CityOrm.name, CityOrm.name_english]

    page_size = 100
    list_template = "sqladmin/list-cities.html"

    column_searchable_list = ["name", "name_english"]

    name = "Город"
    name_plural = "Города"

    column_default_sort = ("id", "desc")
