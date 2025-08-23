from sqlalchemy import Select, select
from sqlalchemy.orm import aliased, joinedload

from src.application.dao.ticket_dao import TicketDAOInterface
from src.application.dto.ticket import TicketFullInfoDTO
from src.entities.tickets.filters import TicketsFilter
from src.entities.value_objects.entity_id import EntityId
from src.infrastructure.persistence.dao.base_dao import BaseDAO
from src.infrastructure.persistence.dao.builders.ticket import TicketFullInfoDTOBuilder
from src.infrastructure.persistence.dao.filters.filters import (
    FirstSegment,
    LastSegment,
    SqlalchemyTicketsFilter,
)
from src.infrastructure.persistence.db.models.models import (
    AirportOrm,
    TicketOrm,
    TicketSegmentOrm,
)


class TicketDAO(BaseDAO, TicketDAOInterface):
    def _ticket_full_info_joins_query(self) -> Select:
        return (
            select(TicketOrm)
            .join(TicketSegmentOrm)
            # .join(FirstSegment, (FirstSegment.ticket_id == TicketOrm.id) & (FirstSegment.segment_number == 1))
            # .join(LastSegment, (LastSegment.ticket_id == TicketOrm.id) & (LastSegment.segment_number == TicketOrm.transfers + 1))
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
            .order_by(TicketOrm.price)
        )

    async def get(self, id: EntityId) -> TicketFullInfoDTO:
        print(id, "ID", type(id))
        result = await self.db.execute(self._ticket_full_info_joins_query().where(TicketOrm.id == id.value))

        ticket = result.scalar()
        print(ticket)
        return TicketFullInfoDTOBuilder.from_orm(ticket) if ticket else None

    async def filter(self, filters: TicketsFilter) -> list[TicketFullInfoDTO]:
        sqlalchemy_filters = SqlalchemyTicketsFilter(**filters.__dict__)
        query = await sqlalchemy_filters.build_query()
        results = await self.db.execute(self._ticket_full_info_joins_query().where(query))
        tickets = results.scalars().unique()

        return [TicketFullInfoDTOBuilder.from_orm(ticket) for ticket in tickets]
