from src.entities.tickets.filters import TicketsFilter
from src.usecases.tickets.filter.dto import TicketFullInfoDTO
from src.usecases.tickets.filter.repository.tickets_repository import (
    TicketReadRepository,
)


class FilterTickets:
    def __init__(self, repository: TicketReadRepository) -> None:
        self.repository = repository

    async def __call__(self, filters: TicketsFilter) -> list[TicketFullInfoDTO]:
        return await self.repository.filter(filters=filters)
