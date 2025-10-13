from decimal import Decimal

from sqlalchemy import Select, and_, or_
from sqlalchemy.orm import aliased

from avia.entities.tickets.filters import TicketsFilter
from avia.infrastructure.persistence.db.models.models import (
    TicketItineraryOrm,
    TicketOrm,
    TicketSegmentOrm,
)


class SqlalchemyTicketsFilter:
    def __init__(self) -> None:
        self._FirstItinerary = aliased(TicketItineraryOrm)
        self._LastItinerary = aliased(TicketItineraryOrm)
        self._FirstSegment = aliased(TicketSegmentOrm)
        self._LastSegment = aliased(TicketSegmentOrm)

    def set_ticket_filters(self, filter: TicketsFilter) -> None:
        self._filter = filter

    def build_max_price_query(self, exchange_rates: dict[str, Decimal]) -> list[and_]:
        return [
            and_(TicketOrm.currency == currency, TicketOrm.price <= self._filter.price_max / amount)  # type: ignore
            for currency, amount in exchange_rates.items()
        ]

    def build_min_price_query(self, exchange_rates: dict[str, Decimal]) -> list[and_]:
        return [
            and_(TicketOrm.currency == currency, TicketOrm.price >= self._filter.price_min / amount)  # type: ignore
            for currency, amount in exchange_rates.items()
        ]

    async def build_price_query(self, exchange_rates: dict[str, Decimal]) -> and_:
        queries = []

        if self._filter.price_min is not None:
            queries.append(and_(or_(*self.build_min_price_query(exchange_rates))))

        if self._filter.price_max is not None:
            queries.append(and_(or_(*self.build_max_price_query(exchange_rates))))

        return queries

    async def build_query(self, exchange_rates: dict[str, Decimal]) -> Select:
        query = and_()
        print(self._filter)

        if self._filter.airline_ids:
            query &= and_(TicketSegmentOrm.airline_id.in_(self._filter.airline_ids))

        if self._filter.origin_airport_ids:
            query &= and_(self._FirstSegment.origin_airport_id.in_(self._filter.origin_airport_ids))

        if self._filter.destination_airport_ids:
            query &= and_(self._LastSegment.destination_airport_id.in_(self._filter.destination_airport_ids))

        if self._filter.transfers:
            query &= and_(TicketItineraryOrm.transfers.in_(self._filter.transfers))

        if self._filter.duration_max:
            query &= and_(TicketItineraryOrm.duration <= self._filter.duration_max)

        if self._filter.duration_min:
            query &= and_(TicketItineraryOrm.duration >= self._filter.duration_min)

        if self._filter.return_at:
            query &= and_(
                TicketSegmentOrm.ticket_itinerary_id == self._LastItinerary.id,
                TicketSegmentOrm.return_at <= self._filter.return_at,
            )

        if self._filter.departure_at:
            query &= and_(
                TicketSegmentOrm.ticket_itinerary_id == self._FirstItinerary.id,
                TicketSegmentOrm.departure_at >= self._filter.departure_at,
            )

        price_queries = await self.build_price_query(exchange_rates)
        for price_query in price_queries:
            query &= price_query

        return query
