from src.infrastructure.admin.model_views.base import BaseModelView
from src.infrastructure.persistence.db.models.models import CountryOrm


class CountryAdmin(BaseModelView, model=CountryOrm):  # type: ignore
    column_list = [CountryOrm.id, CountryOrm.iso, CountryOrm.name, CountryOrm.name_english]

    page_size = 100
    list_template = "sqladmin/list-countries.html"

    column_searchable_list = ["iso"]

    name = "Страна"
    name_plural = "Страны"

    column_default_sort = ("id", "desc")

    form_excluded_columns = ["airports", "regions"]
