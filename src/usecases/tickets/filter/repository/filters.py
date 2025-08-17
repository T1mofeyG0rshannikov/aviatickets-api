from sqlalchemy import Select, and_

from src.entities.tickets.filters import TicketsFilter
from src.infrastructure.db.models.models import TicketOrm


class SqlalchemyTicketsFilter(TicketsFilter):
    def build_query(self) -> Select:
        query = and_()
        if self.origin_airport_ids:
            query &= and_(TicketOrm.origin_airport_id.in_(self.origin_airport_ids))

        if self.destination_airport_ids:
            query &= and_(TicketOrm.destination_airport_id.in_(self.destination_airport_ids))

        if self.transfers:
            query &= and_(TicketOrm.transfers == self.transfers)

        if self.price_min:
            query &= and_(TicketOrm.price >= self.price_min)

        if self.price_max:
            query &= and_(TicketOrm.price <= self.price_max)

        if self.duration_max:
            query &= and_(TicketOrm.duration <= self.duration_max)

        if self.duration_min:
            query &= and_(TicketOrm.duration >= self.duration_min)

        if self.return_at:
            query &= and_(TicketOrm.return_at <= self.return_at)

        if self.departure_at:
            query &= and_(TicketOrm.departure_at >= self.departure_at)

        return query
