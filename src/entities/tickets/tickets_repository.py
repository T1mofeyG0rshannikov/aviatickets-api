from typing import Protocol

from src.entities.tickets.ticket import Ticket
from src.entities.value_objects.entity_id import EntityId


class TicketRepositoryInterface(Protocol):
    async def get(self, id: EntityId) -> Ticket:
        raise NotImplementedError

    async def all(self) -> list[Ticket]:
        raise NotImplementedError

    async def save_many(self, tickets: list[Ticket]) -> None:
        raise NotImplementedError
