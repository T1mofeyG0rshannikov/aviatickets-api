from sqlalchemy import Select, select
from sqlalchemy.orm import joinedload

from src.application.builders.ticket import TicketFullInfoDTOBuilder
from src.application.dto.ticket import TicketFullInfoDTO
from src.application.repositories.tickets_repository import (
    TicketReadRepositoryInterface,
)
from src.entities.tickets.filters import TicketsFilter
from src.infrastructure.db.models.models import AirportOrm, TicketOrm, TicketSegmentOrm
from src.infrastructure.repositories.base_repository import BaseRepository
from src.infrastructure.repositories.filters.filters import SqlalchemyTicketsFilter


class TicketReadRepository(BaseRepository, TicketReadRepositoryInterface):
    def _ticket_full_info_joins_query(self) -> Select:
        return (
            select(TicketOrm)
            .join(TicketSegmentOrm)
            .options(
                joinedload(TicketOrm.segments).joinedload(TicketSegmentOrm.origin_airport).joinedload(AirportOrm.city),
                joinedload(TicketOrm.segments)
                .joinedload(TicketSegmentOrm.origin_airport)
                .joinedload(AirportOrm.country),
                joinedload(TicketOrm.segments)
                .joinedload(TicketSegmentOrm.origin_airport)
                .joinedload(AirportOrm.region),
                joinedload(TicketOrm.segments)
                .joinedload(TicketSegmentOrm.destination_airport)
                .joinedload(AirportOrm.city),
                joinedload(TicketOrm.segments)
                .joinedload(TicketSegmentOrm.destination_airport)
                .joinedload(AirportOrm.country),
                joinedload(TicketOrm.segments)
                .joinedload(TicketSegmentOrm.destination_airport)
                .joinedload(AirportOrm.region),
                joinedload(TicketOrm.segments).joinedload(TicketSegmentOrm.airline),
            )
        )

    async def get(self, id: int) -> TicketFullInfoDTO:
        result = await self.db.execute(self._ticket_full_info_joins_query().where(TicketOrm.id == id))

        ticket = result.scalar()
        return TicketFullInfoDTOBuilder.from_orm(ticket) if ticket else None

    async def filter(self, filters: TicketsFilter) -> list[TicketFullInfoDTO]:
        sqlalchemy_filters = SqlalchemyTicketsFilter(**filters.__dict__)
        query = await sqlalchemy_filters.build_query()
        results = await self.db.execute(self._ticket_full_info_joins_query().where(query))
        tickets = results.scalars().unique()

        return [TicketFullInfoDTOBuilder.from_orm(ticket) for ticket in tickets]
