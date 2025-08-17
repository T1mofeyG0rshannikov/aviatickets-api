from sqlalchemy import Select, select
from sqlalchemy.orm import joinedload

from src.entities.tickets.filters import TicketsFilter
from src.infrastructure.db.models.models import AirportOrm, TicketOrm
from src.infrastructure.repositories.base_reposiotory import BaseRepository
from src.usecases.tickets.filter.builders import TicketFullInfoDTOBuilder
from src.usecases.tickets.filter.dto import TicketFullInfoDTO
from src.usecases.tickets.filter.repository.filters import SqlalchemyTicketsFilter


class TicketReadRepository(BaseRepository):
    def _ticket_full_info_joins_query(self) -> Select:
        return select(TicketOrm).options(
            joinedload(TicketOrm.origin_airport).joinedload(AirportOrm.city),
            joinedload(TicketOrm.origin_airport).joinedload(AirportOrm.country),
            joinedload(TicketOrm.origin_airport).joinedload(AirportOrm.region),
            joinedload(TicketOrm.destination_airport).joinedload(AirportOrm.city),
            joinedload(TicketOrm.destination_airport).joinedload(AirportOrm.country),
            joinedload(TicketOrm.destination_airport).joinedload(AirportOrm.region),
            joinedload(TicketOrm.airline),
        )

    async def get(self, id: int) -> TicketFullInfoDTO:
        result = await self.db.execute(self._ticket_full_info_joins_query().where(TicketOrm.id == id))

        ticket = result.scalar()
        return TicketFullInfoDTOBuilder.from_orm(ticket)

    async def filter(self, filters: TicketsFilter) -> list[TicketFullInfoDTO]:
        sqlalchemy_filters = SqlalchemyTicketsFilter(**filters.__dict__)
        query = sqlalchemy_filters.build_query()

        results = await self.db.execute(self._ticket_full_info_joins_query().where(query))
        tickets = results.scalars().all()

        return [TicketFullInfoDTOBuilder.from_orm(ticket) for ticket in tickets]
