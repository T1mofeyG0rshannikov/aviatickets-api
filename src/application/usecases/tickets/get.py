from src.application.dto.ticket import TicketFullInfoDTO
from src.application.repositories.tickets_repository import (
    TicketReadRepositoryInterface,
)
from src.entities.tickets.exceptions import TicketNotFoundError


class GetTicket:
    def __init__(self, ticket_repository: TicketReadRepositoryInterface) -> None:
        self.repository = ticket_repository

    async def __call__(self, ticket_id: int) -> TicketFullInfoDTO:
        ticket = await self.repository.get(ticket_id)
        if ticket is None:
            raise TicketNotFoundError(f"Нет билета с id='{ticket_id}'")

        return ticket
