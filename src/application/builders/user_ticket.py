from src.application.dto.user_ticket import UserTicketFullInfoDTO
from src.application.repositories.tickets_repository import (
    TicketReadRepositoryInterface,
)
from src.entities.user_ticket.user_ticket import UserTicket
from src.infrastructure.repositories.user_repository import UserRepository
from src.infrastructure.repositories.user_ticket_repository import UserTicketRepository


class UserTicketFullInfoAssembler:
    def __init__(
        self,
        user_repository: UserRepository,
        ticket_repository: TicketReadRepositoryInterface,
        user_ticket_repository: UserTicketRepository,
    ) -> None:
        self.user_repository = user_repository
        self.ticket_repository = ticket_repository
        self.user_ticket_repository = user_ticket_repository

    async def execute(self, user_ticket: UserTicket) -> UserTicketFullInfoDTO:
        user = await self.user_repository.get(id=user_ticket.user_id)
        ticket = await self.ticket_repository.get(id=user_ticket.ticket_id)
        passengers = await self.user_ticket_repository.get_passangers(user_ticket.id)

        return UserTicketFullInfoDTO(id=user_ticket.id, user=user, ticket=ticket, passengers=passengers)
