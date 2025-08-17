from src.admin.model_views.base import BaseModelView
from src.infrastructure.db.models.models import TicketOrm


class TicketAdmin(BaseModelView, model=TicketOrm):
    column_list = [
        TicketOrm.id,
        TicketOrm.origin_airport,
        TicketOrm.destination_airport,
        TicketOrm.airline,
        TicketOrm.departure_at,
        TicketOrm.return_at,
        TicketOrm.duration,
        TicketOrm.price,
        TicketOrm.transfers,
    ]

    page_size = 100

    name = "Билет"
    name_plural = "Билеты"

    column_default_sort = ("id", "desc")
