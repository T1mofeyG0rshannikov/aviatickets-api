from uuid import UUID

from src.application.dto.user_ticket import CreatePassengerDTO
from src.application.factories.user_ticket_factory import UserTicketFactory
from src.entities.exceptions import AccessDeniedError, InvalidcredentialsError
from src.entities.tickets.exceptions import TicketNotFoundError
from src.entities.tickets.tickets_repository import TicketRepositoryInterface
from src.entities.user.user import User
from src.entities.user_ticket.exceptions import (
    ExpiredInternationalPassportError,
    InvalidInternationalPassportError,
)
from src.entities.user_ticket.user_ticket import Passenger
from src.entities.user_ticket.user_ticket_repository import (
    UserTicketRepositoryInterface,
)
from src.entities.value_objects.entity_id import EntityId


class CreateUserTicket:
    def __init__(self, repository: UserTicketRepositoryInterface, ticket_repository: TicketRepositoryInterface) -> None:
        self.repository = repository
        self.ticket_repository = ticket_repository

    async def __call__(self, ticket_id: UUID, passangers_to_create: list[CreatePassengerDTO], user: User) -> None:
        user_ticket = UserTicketFactory.create(user_id=user.id.value, ticket_id=ticket_id)

        passengers = []

        for passenger in passangers_to_create:
            try:
                passengers.append(Passenger.create(user_ticket_id=user_ticket.id, **passenger.__dict__))
            except InvalidInternationalPassportError:
                raise InvalidInternationalPassportError(
                    f"{passenger.first_name} {passenger.second_name}: Неправильный номер загран паспорта - {passenger.passport}"
                )

            except ExpiredInternationalPassportError:
                raise ExpiredInternationalPassportError(
                    f"У пассажира {passenger.first_name} {passenger.second_name} истёк срок загран. паспорта"
                )

        ticket = await self.ticket_repository.get(id=ticket_id)
        if ticket is None:
            raise TicketNotFoundError(f"Нет билета с id='{ticket_id}'")

        await self.repository.save(user_ticket=user_ticket, passengers=passengers)
