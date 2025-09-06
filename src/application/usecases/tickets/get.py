from src.application.dto.ticket import TicketFullInfoDTO
from src.application.persistence.dao.ticket_dao import TicketDAOInterface
from src.entities.tickets.exceptions import TicketNotFoundError
from src.entities.value_objects.entity_id import EntityId


class GetTicket:
    def __init__(self, ticket_dao: TicketDAOInterface) -> None:
        self.dao = ticket_dao

    async def __call__(self, ticket_id: EntityId) -> TicketFullInfoDTO:
        ticket = await self.dao.get(ticket_id)
        if ticket is None:
            raise TicketNotFoundError(f"Нет билета с id='{ticket_id}'")

        return ticket
