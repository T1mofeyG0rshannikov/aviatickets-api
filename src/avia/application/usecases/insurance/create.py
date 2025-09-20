from avia.application.persistence.transaction import Transaction
from avia.entities.exceptions import AccessDeniedError
from avia.entities.insurance.insurance import Insurance
from avia.entities.insurance.repository import InsuranceRepositoryInterface
from avia.entities.location.exceptions import CountryNotFoundError
from avia.entities.location.location_repository import LocationRepositoryInterface
from avia.entities.tickets.exceptions import TicketNotFoundError
from avia.entities.tickets.tickets_repository import TicketRepositoryInterface
from avia.entities.user.user import User
from avia.entities.user_ticket.exceptions import UserTicketNotFoundError
from avia.entities.user_ticket.user_ticket_repository import (
    UserTicketRepositoryInterface,
)
from avia.entities.value_objects.entity_id import EntityId


class CreateInsurance:
    def __init__(
        self,
        transaction: Transaction,
        repository: InsuranceRepositoryInterface,
        user_ticket_repository: UserTicketRepositoryInterface,
        ticket_repository: TicketRepositoryInterface,
        location_repository: LocationRepositoryInterface,
    ) -> None:
        self.repository = repository
        self.user_ticket_repository = user_ticket_repository
        self.ticket_repository = ticket_repository
        self.transaction = transaction
        self.location_repository = location_repository

    async def __call__(self, user_ticket_id: EntityId, user: User) -> Insurance:
        user_ticket = await self.user_ticket_repository.get(id=user_ticket_id)

        if user_ticket is None:
            raise UserTicketNotFoundError(f"Нет пользовательского билета с id='{user_ticket_id}'")

        if user_ticket.user_id != user.id:
            raise AccessDeniedError("Вы не можете получать страховку на чужой билет")

        ticket = await self.ticket_repository.get(id=user_ticket.ticket_id)
        if ticket is None:
            raise TicketNotFoundError(f"Нет билета с id='{user_ticket.ticket_id}'")

        destination_country = await self.location_repository.get_country_by_id(ticket.destination_country_id)
        if destination_country is None:
            raise CountryNotFoundError(f"country with id='{ticket.destination_country_id}' not found")

        insurance = Insurance.create(insured_id=user.id, ticket=ticket, territory=destination_country.name_english)

        await self.repository.save(insurance)
        await self.transaction.commit()
        return insurance
