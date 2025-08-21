from src.infrastructure.admin.model_views.base import BaseModelView
from src.infrastructure.db.models.models import RegionOrm


class RegionAdmin(BaseModelView, model=RegionOrm):
    column_list = [
        RegionOrm.id,
        RegionOrm.iso,
        RegionOrm.name,
        RegionOrm.name_english,
        RegionOrm.country_id,
    ]

    page_size = 100
    list_template = "sqladmin/list-regions.html"

    column_searchable_list = ["iso"]

    name = "Регион"
    name_plural = "Регионы"

    column_default_sort = ("id", "desc")
