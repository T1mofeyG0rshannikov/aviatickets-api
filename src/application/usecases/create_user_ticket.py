from datetime import datetime

from src.entities.tickets.exceptions import TicketNotFoundError
from src.entities.user.user import User
from src.entities.user_ticket.dto import CreatePassengerDTO
from src.entities.user_ticket.exceptions import ExpiredInternationalPassportError
from src.infrastructure.repositories.tickets_repository import TicketRepository
from src.infrastructure.repositories.user_ticket_repository import UserTicketRepository


class CreateUserTicket:
    def __init__(self, repository: UserTicketRepository, ticket_repository: TicketRepository) -> None:
        self.repository = repository
        self.ticket_repository = ticket_repository

    async def __call__(self, ticket_id: int, passangers: list[CreatePassengerDTO], user: User) -> None:
        ticket = await self.ticket_repository.get(id=ticket_id)
        if ticket is None:
            raise TicketNotFoundError(f"Нет билета с id='{ticket_id}'")

        for passenger in passangers:
            if passenger.expiration_date.date() <= datetime.today().date():
                raise ExpiredInternationalPassportError(
                    f"У пассажира {passenger.first_name} {passenger.second_name} истёк срок загран. паспорта"
                )

        await self.repository.create(user_id=user.id, ticket_id=ticket_id, passengers=passangers)
