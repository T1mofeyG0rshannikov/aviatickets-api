from decimal import Decimal
from typing import Protocol

from avia.application.dto.ticket import TicketFullInfoDTO
from avia.entities.tickets.filters import TicketsFilter
from avia.entities.value_objects.entity_id import EntityId


class TicketDAOInterface(Protocol):
    async def get(self, id: EntityId) -> TicketFullInfoDTO | None:
        raise NotImplementedError

    async def filter(self, filters: TicketsFilter, exchange_rates: dict[str, Decimal]) -> list[TicketFullInfoDTO]:
        raise NotImplementedError
