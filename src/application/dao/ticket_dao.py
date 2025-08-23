from typing import Protocol

from src.application.dto.ticket import TicketFullInfoDTO
from src.entities.tickets.filters import TicketsFilter
from src.entities.value_objects.entity_id import EntityId


class TicketDAOInterface(Protocol):
    async def get(self, id: EntityId) -> TicketFullInfoDTO:
        raise NotImplementedError

    async def filter(self, filters: TicketsFilter) -> list[TicketFullInfoDTO]:
        raise NotImplementedError
