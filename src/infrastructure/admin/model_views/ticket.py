from typing import Any

from fastapi import Request
from fastapi.responses import RedirectResponse
from sqladmin import action
from sqladmin.helpers import slugify_class_name
from sqlalchemy import delete
from sqlalchemy.orm import joinedload

from src.infrastructure.admin.model_views.base import BaseModelView
from src.infrastructure.persistence.db.database import new_session
from src.infrastructure.persistence.db.models.models import (
    PassengerOrm,
    TicketItineraryOrm,
    TicketOrm,
    TicketSegmentOrm,
    UserTicketOrm,
)


class TicketAdmin(BaseModelView, model=TicketOrm):  # type: ignore
    # column_list = [TicketOrm.id, TicketOrm.price, TicketOrm.currency]
    column_list = [TicketOrm.id, TicketOrm.unique_key, TicketOrm.price, TicketOrm.currency]
    page_size = 100

    name = "Билет"
    name_plural = "Билеты"

    column_default_sort = ("id", "desc")

    async def get_object_for_details(self, value: Any) -> Any:
        stmt = self._stmt_by_identifier(value).options(
            joinedload(TicketOrm.itineraries)
            .joinedload(TicketItineraryOrm.segments)
            .joinedload(TicketSegmentOrm.destination_airport),
            joinedload(TicketOrm.itineraries)
            .joinedload(TicketItineraryOrm.segments)
            .joinedload(TicketSegmentOrm.origin_airport),
        )

        return await self._get_object_by_pk(stmt)

    @action(name="delete_all", label="Удалить", confirmation_message="Вы уверены?")
    async def delete_all_action(self, request: Request):
        async with self.session_maker(expire_on_commit=False) as session:
            await session.execute(delete(PassengerOrm))
            await session.execute(delete(UserTicketOrm))
            await session.execute(delete(TicketSegmentOrm))
            await session.execute(delete(TicketItineraryOrm))
            await session.execute(delete(self.model))
            await session.commit()
            return RedirectResponse(url=f"/admin/{slugify_class_name(self.model.__name__)}/list", status_code=303)

    async def on_model_delete(self, model: Any, request: Request) -> None:
        """Perform some actions before a model is deleted.
        By default does nothing.
        """
        async with new_session() as session:
            await session.execute(
                delete(TicketSegmentOrm).where(TicketSegmentOrm.ticket_itinerary.has(ticket_id=model.id))
            )
            await session.commit()
            await session.close()


class TicketItineraryAdmin(BaseModelView, model=TicketItineraryOrm):  # type: ignore
    # column_list = [
    #    TicketItineraryOrm.id,
    #    TicketItineraryOrm.duration,
    #    TicketItineraryOrm.ticket_id,
    #    TicketItineraryOrm.ticket,
    #    TicketItineraryOrm.transfers,
    # ]

    column_list = [
        TicketItineraryOrm.id,
        TicketItineraryOrm.duration,
        TicketItineraryOrm.ticket_id,
        TicketItineraryOrm.transfers,
    ]

    page_size = 100

    column_default_sort = ("id", "desc")

    async def get_object_for_details(self, value: Any) -> Any:
        stmt = self._stmt_by_identifier(value).options(
            joinedload(TicketItineraryOrm.segments).joinedload(TicketSegmentOrm.destination_airport),
            joinedload(TicketItineraryOrm.segments).joinedload(TicketSegmentOrm.origin_airport),
        )

        return await self._get_object_by_pk(stmt)


class TicketSegmentAdmin(BaseModelView, model=TicketSegmentOrm):  # type: ignore
    # column_list = [
    #    TicketSegmentOrm.id,
    #    TicketSegmentOrm.segment_number,
    #    TicketSegmentOrm.duration,
    #    TicketSegmentOrm.origin_airport_id,
    #    TicketSegmentOrm.destination_airport_id,
    #    TicketSegmentOrm.airline_id,
    #    TicketSegmentOrm.departure_at,
    #    TicketSegmentOrm.return_at,
    #    TicketSegmentOrm.flight_number,
    #    TicketSegmentOrm.status,
    #    TicketSegmentOrm.seat_class,
    #    TicketSegmentOrm.ticket_itinerary_id,
    # ]

    column_list = [
        TicketSegmentOrm.id,
        TicketSegmentOrm.origin_airport_id,
        TicketSegmentOrm.destination_airport_id,
        TicketSegmentOrm.airline_id,
        TicketSegmentOrm.aircraft_id,
        TicketSegmentOrm.departure_at,
        TicketSegmentOrm.return_at,
        TicketSegmentOrm.duration,
        TicketSegmentOrm.flight_number,
        TicketSegmentOrm.segment_number,
        TicketSegmentOrm.status,
        TicketSegmentOrm.seat_class,
        TicketSegmentOrm.ticket_itinerary_id,
    ]

    page_size = 100

    # name = "Билет"
    # name_plural = "Билеты"

    column_default_sort = ("id", "desc")
