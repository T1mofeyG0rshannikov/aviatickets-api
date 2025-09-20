from typing import Protocol

from avia.entities.user_ticket.user_ticket import UserTicket
from avia.entities.value_objects.entity_id import EntityId


class UserTicketRepositoryInterface(Protocol):
    async def get(self, id: EntityId) -> UserTicket | None:
        raise NotImplementedError

    async def save(self, user_ticket: UserTicket) -> None:
        raise NotImplementedError
