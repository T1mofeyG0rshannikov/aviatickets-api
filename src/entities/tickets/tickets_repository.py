from typing import Protocol

from src.entities.tickets.ticket_entity.ticket import Ticket
from src.entities.tickets.value_objects.unique_key import TicketUniqueKey
from src.entities.value_objects.entity_id import EntityId


class TicketRepositoryInterface(Protocol):
    async def get(self, id: EntityId) -> Ticket | None:
        raise NotImplementedError

    async def save_many(self, tickets: list[Ticket]) -> None:
        raise NotImplementedError

    async def all_unique_keys(self) -> set[TicketUniqueKey]:
        raise NotImplementedError
