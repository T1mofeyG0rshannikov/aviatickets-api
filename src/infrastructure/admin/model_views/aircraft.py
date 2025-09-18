from src.infrastructure.admin.model_views.base import BaseModelView
from src.infrastructure.persistence.db.models.models import AircraftOrm


class AircraftAdmin(BaseModelView, model=AircraftOrm):  # type: ignore
    column_list = [AircraftOrm.id, AircraftOrm.iata, AircraftOrm.name, AircraftOrm.wtc]

    page_size = 100
    list_template = "sqladmin/list-aircrafts.html"

    column_searchable_list = ["icao", "iata"]

    name = "Самолёт"
    name_plural = "Самолёты"

    column_default_sort = ("iata", "desc")
