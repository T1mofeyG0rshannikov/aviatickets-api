from decimal import Decimal

from sqlalchemy import Select, select
from sqlalchemy.orm import joinedload

from avia.application.dto.ticket import TicketFullInfoDTO
from avia.application.persistence.dao.ticket_dao import TicketDAOInterface
from avia.entities.tickets.filters import TicketsFilter
from avia.entities.value_objects.entity_id import EntityId
from avia.infrastructure.persistence.dao.builders.list_ticket import ListTicketDTOBuilder
from avia.infrastructure.persistence.dao.builders.ticket import TicketFullInfoDTOBuilder
from avia.infrastructure.persistence.dao.filters.filters import SqlalchemyTicketsFilter
from avia.infrastructure.persistence.db.models.models import (
    AirportOrm,
    TicketItineraryOrm,
    TicketOrm,
    TicketSegmentOrm,
)
from avia.infrastructure.persistence.persist_base import PersistenceBase
from sqlalchemy.ext.asyncio import AsyncSession


class TicketDAO(PersistenceBase, TicketDAOInterface):
    def __init__(self, db: AsyncSession, filter_builder: SqlalchemyTicketsFilter) -> None:
        super().__init__(db)
        self._filter_builder = filter_builder

    def _ticket_full_info_joins_query(self) -> Select:
        return (
            select(TicketOrm)
            .options(
                joinedload(TicketOrm.itineraries)
                .joinedload(TicketItineraryOrm.segments)
                .joinedload(TicketSegmentOrm.origin_airport)
                .joinedload(AirportOrm.city),
                joinedload(TicketOrm.itineraries)
                .joinedload(TicketItineraryOrm.segments)
                .joinedload(TicketSegmentOrm.origin_airport)
                .joinedload(AirportOrm.country),
                joinedload(TicketOrm.itineraries)
                .joinedload(TicketItineraryOrm.segments)
                .joinedload(TicketSegmentOrm.origin_airport)
                .joinedload(AirportOrm.region),
                joinedload(TicketOrm.itineraries)
                .joinedload(TicketItineraryOrm.segments)
                .joinedload(TicketSegmentOrm.destination_airport)
                .joinedload(AirportOrm.city),
                joinedload(TicketOrm.itineraries)
                .joinedload(TicketItineraryOrm.segments)
                .joinedload(TicketSegmentOrm.destination_airport)
                .joinedload(AirportOrm.country),
                joinedload(TicketOrm.itineraries)
                .joinedload(TicketItineraryOrm.segments)
                .joinedload(TicketSegmentOrm.destination_airport)
                .joinedload(AirportOrm.region),
                joinedload(TicketOrm.itineraries)
                .joinedload(TicketItineraryOrm.segments)
                .joinedload(TicketSegmentOrm.airline),
                joinedload(TicketOrm.itineraries)
                .joinedload(TicketItineraryOrm.segments)
                .joinedload(TicketSegmentOrm.aircraft),
            )
        )
    
    def _list_ticket_joins_query(self) -> Select:
        return (
            select(TicketOrm)
            .join(self._filter_builder._FirstItinerary, TicketOrm.itineraries)
            .join(self._filter_builder._FirstSegment, self._filter_builder._FirstItinerary.segments)
            .join(self._filter_builder._LastItinerary, TicketOrm.itineraries)
            .join(self._filter_builder._LastSegment, self._filter_builder._LastItinerary.segments)
            .options(
                joinedload(TicketOrm.itineraries)
                .joinedload(TicketItineraryOrm.segments)
                .joinedload(TicketSegmentOrm.origin_airport)
                .joinedload(AirportOrm.city),
                joinedload(TicketOrm.itineraries)
                .joinedload(TicketItineraryOrm.segments)
                .joinedload(TicketSegmentOrm.origin_airport)
                .joinedload(AirportOrm.country),
                joinedload(TicketOrm.itineraries)
                .joinedload(TicketItineraryOrm.segments)
                .joinedload(TicketSegmentOrm.origin_airport)
                .joinedload(AirportOrm.region),
                joinedload(TicketOrm.itineraries)
                .joinedload(TicketItineraryOrm.segments)
                .joinedload(TicketSegmentOrm.destination_airport)
                .joinedload(AirportOrm.city),
                joinedload(TicketOrm.itineraries)
                .joinedload(TicketItineraryOrm.segments)
                .joinedload(TicketSegmentOrm.destination_airport)
                .joinedload(AirportOrm.country),
                joinedload(TicketOrm.itineraries)
                .joinedload(TicketItineraryOrm.segments)
                .joinedload(TicketSegmentOrm.destination_airport)
                .joinedload(AirportOrm.region),
                joinedload(TicketOrm.itineraries)
                .joinedload(TicketItineraryOrm.segments)
                .joinedload(TicketSegmentOrm.airline),
                joinedload(TicketOrm.itineraries)
                .joinedload(TicketItineraryOrm.segments)
                .joinedload(TicketSegmentOrm.aircraft),
            )
            .order_by(TicketOrm.price)
        )

    async def get(self, id: EntityId) -> TicketFullInfoDTO | None:
        result = await self.db.execute(self._ticket_full_info_joins_query().where(TicketOrm.id == id.value).distinct())

        ticket = result.scalar()
        return TicketFullInfoDTOBuilder.from_orm(ticket) if ticket else None

    async def filter(self, filters: TicketsFilter, exchange_rates: dict[str, Decimal]) -> list[TicketFullInfoDTO]:
        self._filter_builder.set_ticket_filters(filters)
        query = await self._filter_builder.build_query(exchange_rates)
        print("start query")
        results = await self.db.execute(self._list_ticket_joins_query().where(query).distinct())
        tickets = results.scalars().unique()
        print("end query")

        return [ListTicketDTOBuilder.from_orm(ticket) for ticket in tickets]
