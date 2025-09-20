from avia.application.dto.user_ticket import CreatePassengerDTO
from avia.application.factories.user_ticket_factory import UserTicketFactory
from avia.application.persistence.transaction import Transaction
from avia.entities.tickets.exceptions import TicketNotFoundError
from avia.entities.tickets.tickets_repository import TicketRepositoryInterface
from avia.entities.user.user import User
from avia.entities.user_ticket.user_ticket_repository import (
    UserTicketRepositoryInterface,
)
from avia.entities.value_objects.entity_id import EntityId


class CreateUserTicket:
    def __init__(
        self,
        repository: UserTicketRepositoryInterface,
        ticket_repository: TicketRepositoryInterface,
        transaction: Transaction,
    ) -> None:
        self.repository = repository
        self.ticket_repository = ticket_repository
        self.transaction = transaction

    async def __call__(self, ticket_id: EntityId, passengers_to_create: list[CreatePassengerDTO], user: User) -> None:
        ticket = await self.ticket_repository.get(id=ticket_id)
        if ticket is None:
            raise TicketNotFoundError(f"Нет билета с id='{ticket_id}'")

        user_ticket = UserTicketFactory.create(
            user_id=user.id, ticket_id=ticket_id, passengers_dto=passengers_to_create
        )

        await self.repository.save(user_ticket=user_ticket)
        await self.transaction.commit()
