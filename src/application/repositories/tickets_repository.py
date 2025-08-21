from typing import Protocol

from src.application.dto.ticket import TicketFullInfoDTO
from src.entities.tickets.filters import TicketsFilter


class TicketReadRepositoryInterface(Protocol):
    async def get(self, id: int) -> TicketFullInfoDTO:
        raise NotImplementedError

    async def filter(self, filters: TicketsFilter) -> list[TicketFullInfoDTO]:
        raise NotImplementedError
