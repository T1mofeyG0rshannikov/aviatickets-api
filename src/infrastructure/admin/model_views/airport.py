from src.infrastructure.admin.model_views.base import BaseModelView
from src.infrastructure.persistence.db.models.models import AirportOrm


class AirportAdmin(BaseModelView, model=AirportOrm):  # type: ignore
    column_list = [
        AirportOrm.id,
        AirportOrm.name,
        AirportOrm.continent,
        AirportOrm.country_id,
        AirportOrm.region_id,
        AirportOrm.city_id,
        AirportOrm.scheduled_service,
        AirportOrm.icao,
        AirportOrm.iata,
        AirportOrm.gps_code,
        AirportOrm.local_code,
        AirportOrm.name_russian,
    ]

    page_size = 100
    list_template = "sqladmin/list-airports.html"

    column_searchable_list = ["id", "icao", "iata"]

    name = "Аэропорт"
    name_plural = "Аэропорты"

    column_default_sort = ("id", "desc")
