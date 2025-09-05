from decimal import Decimal

from sqlalchemy import Select, and_, or_
from sqlalchemy.orm import aliased

from src.entities.tickets.filters import TicketsFilter
from src.infrastructure.persistence.db.models.models import TicketOrm, TicketSegmentOrm

FirstSegment = aliased(TicketSegmentOrm)
LastSegment = aliased(TicketSegmentOrm)


class SqlalchemyTicketsFilter(TicketsFilter):
    def build_max_price_query(self, exchange_rates: dict[str, Decimal]) -> list[and_]:
        return [
            and_(TicketOrm.currency == currency, TicketOrm.price <= self.price_max / amount)  # type: ignore
            for currency, amount in exchange_rates.items()
        ]

    def build_min_price_query(self, exchange_rates: dict[str, Decimal]) -> list[and_]:
        return [
            and_(TicketOrm.currency == currency, TicketOrm.price >= self.price_min / amount)  # type: ignore
            for currency, amount in exchange_rates.items()
        ]

    async def build_price_query(self, exchange_rates: dict[str, Decimal]) -> and_:
        queries = []

        if self.price_min is not None:
            queries.append(and_(or_(*self.build_min_price_query(exchange_rates))))

        if self.price_max is not None:
            queries.append(and_(or_(*self.build_max_price_query(exchange_rates))))

        return queries

    async def build_query(self, exchange_rates: dict[str, Decimal]) -> Select:
        query = and_()

        if self.origin_airport_ids:
            query &= and_(FirstSegment.origin_airport_id.in_(self.origin_airport_ids))

        if self.destination_airport_ids:
            query &= and_(LastSegment.destination_airport_id.in_(self.destination_airport_ids))

        if self.transfers:
            query &= and_(TicketOrm.transfers == self.transfers)

        if self.duration_max:
            query &= and_(TicketOrm.duration <= self.duration_max)

        if self.duration_min:
            query &= and_(TicketOrm.duration >= self.duration_min)

        if self.return_at:
            query &= and_(LastSegment.return_at <= self.return_at)

        if self.departure_at:
            query &= and_(FirstSegment.departure_at >= self.departure_at)

        price_queries = await self.build_price_query(exchange_rates)
        for price_query in price_queries:
            query &= price_query

        return query
