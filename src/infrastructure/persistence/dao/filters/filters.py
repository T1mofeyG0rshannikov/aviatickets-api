from typing import Annotated, Self

from sqlalchemy import Select, and_, or_
from sqlalchemy.orm import aliased

from src.entities.tickets.filters import TicketsFilter
from src.infrastructure.clients.exchange_rates.exchange_rates_service import (
    ExchangeRateService,
)
from src.infrastructure.depends.base import get_exchange_rate_service
from src.infrastructure.depends.decorator import inject_dependencies
from src.infrastructure.persistence.db.models.models import TicketOrm, TicketSegmentOrm

FirstSegment = aliased(TicketSegmentOrm)
LastSegment = aliased(TicketSegmentOrm)


class SqlalchemyTicketsFilter(TicketsFilter):
    def build_max_price_query(self, exchange_rates: dict[str, float]) -> list[and_]:
        return [
            and_(TicketOrm.currency == currency, TicketOrm.price <= self.price_max / amount)
            for currency, amount in exchange_rates.items()
        ]

    def build_min_price_query(self, exchange_rates: dict[str, float]) -> list[and_]:
        return [
            and_(TicketOrm.currency == currency, TicketOrm.price >= self.price_min / amount)
            for currency, amount in exchange_rates.items()
        ]

    @inject_dependencies
    async def build_price_query(
        self: Self, exchange_rate_service: Annotated[ExchangeRateService, get_exchange_rate_service]
    ) -> and_:
        exchange_rates = await exchange_rate_service.get()

        queries = []

        if self.price_min is not None:
            queries.append(and_(or_(*self.build_min_price_query(exchange_rates))))

        if self.price_max is not None:
            queries.append(and_(or_(*self.build_max_price_query(exchange_rates))))

        return queries

    async def build_query(self) -> Select:
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
            query &= and_(TicketSegmentOrm.return_at <= self.return_at)

        if self.departure_at:
            query &= and_(TicketSegmentOrm.departure_at >= self.departure_at)

        price_queries = await self.build_price_query()
        for price_query in price_queries:
            query &= price_query

        return query
