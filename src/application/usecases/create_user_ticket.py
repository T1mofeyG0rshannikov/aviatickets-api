from src.application.dto.user_ticket import CreatePassengerDTO
from src.application.factories.user_ticket_factory import UserTicketFactory
from src.entities.tickets.exceptions import TicketNotFoundError
from src.entities.tickets.tickets_repository import TicketRepositoryInterface
from src.entities.user.user import User
from src.entities.user_ticket.user_ticket_repository import (
    UserTicketRepositoryInterface,
)
from src.entities.value_objects.entity_id import EntityId


class CreateUserTicket:
    def __init__(self, repository: UserTicketRepositoryInterface, ticket_repository: TicketRepositoryInterface) -> None:
        self.repository = repository
        self.ticket_repository = ticket_repository

    async def __call__(self, ticket_id: EntityId, passengers_to_create: list[CreatePassengerDTO], user: User) -> None:
        ticket = await self.ticket_repository.get(id=ticket_id)
        if ticket is None:
            raise TicketNotFoundError(f"Нет билета с id='{ticket_id}'")

        user_ticket = UserTicketFactory.create(
            user_id=user.id, ticket_id=ticket_id, passengers_dto=passengers_to_create
        )

        await self.repository.save(user_ticket=user_ticket)
