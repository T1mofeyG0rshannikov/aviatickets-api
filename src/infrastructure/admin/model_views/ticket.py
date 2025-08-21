from src.infrastructure.admin.model_views.base import BaseModelView
from src.infrastructure.db.models.models import TicketOrm, TicketSegmentOrm


class TicketAdmin(BaseModelView, model=TicketOrm):
    column_list = [TicketOrm.id, TicketOrm.duration, TicketOrm.price, TicketOrm.transfers, TicketOrm.currency]

    page_size = 100

    name = "Билет"
    name_plural = "Билеты"

    column_default_sort = ("id", "desc")


class TicketSegmentAdmin(BaseModelView, model=TicketSegmentOrm):
    column_list = [
        TicketSegmentOrm.id,
        TicketSegmentOrm.duration,
        TicketSegmentOrm.origin_airport_id,
        TicketSegmentOrm.destination_airport_id,
        TicketSegmentOrm.airline_id,
        TicketSegmentOrm.departure_at,
        TicketSegmentOrm.return_at,
        TicketSegmentOrm.flight_number,
        TicketSegmentOrm.status,
        TicketSegmentOrm.seat_class,
        TicketSegmentOrm.ticket_id,
    ]

    page_size = 100

    # name = "Билет"
    # name_plural = "Билеты"

    column_default_sort = ("id", "desc")
