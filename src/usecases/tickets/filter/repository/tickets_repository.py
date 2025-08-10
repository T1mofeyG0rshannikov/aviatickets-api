from typing import List

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.db.mappers.airline import from_orm_to_airline
from src.db.mappers.airport import orm_to_airport
from src.db.models.models import TicketOrm
from src.entities.tickets.filters import TicketsFilter
from src.repositories.base_reposiotory import BaseRepository
from src.usecases.tickets.filter.dto import TicketFullInfoDTO
from src.usecases.tickets.filter.repository.filters import SqlalchemyTicketsFilter


class TicketFullInfoDTOBuilder:
    @classmethod
    def from_orm(cls, ticket: TicketOrm) -> TicketFullInfoDTO:
        return TicketFullInfoDTO(
            id=ticket.id,
            origin_airport=orm_to_airport(ticket.origin_airport),
            destination_airport=orm_to_airport(ticket.destination_airport),
            airline=from_orm_to_airline(ticket.airline),
            departure_at=ticket.departure_at,
            return_at=ticket.return_at,
            duration=ticket.duration,
            price=ticket.price,
            transfers=ticket.transfers,
        )


class TicketReadRepository(BaseRepository):
    async def filter(self, filters: TicketsFilter) -> list[TicketFullInfoDTO]:
        sqlalchemy_filters = SqlalchemyTicketsFilter(**filters.__dict__)
        query = sqlalchemy_filters.build_query()
        print(query)
        results = await self.db.execute(
            select(TicketOrm)
            .options(
                joinedload(TicketOrm.origin_airport),
                joinedload(TicketOrm.destination_airport),
                joinedload(TicketOrm.airline),
            )
            .where(query)
        )
        tickets = results.scalars().all()

        return [TicketFullInfoDTOBuilder.from_orm(ticket) for ticket in tickets]
