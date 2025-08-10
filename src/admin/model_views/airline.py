from src.admin.model_views.base import BaseModelView
from src.db.models.models import AirlineOrm


class AirlineAdmin(BaseModelView, model=AirlineOrm):
    column_list = [AirlineOrm.id, AirlineOrm.icao, AirlineOrm.iata, AirlineOrm.name, AirlineOrm.name_russian]

    page_size = 100
    list_template = "sqladmin/list-airlines.html"

    column_searchable_list = ["icao", "iata"]

    name = "Авиакомпания"
    name_plural = "Авиакомпании"

    column_default_sort = ("id", "desc")
