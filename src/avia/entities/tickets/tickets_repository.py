from typing import Protocol

from avia.entities.tickets.ticket_entity.ticket import Ticket
from avia.entities.tickets.value_objects.unique_key import TicketUniqueKey
from avia.entities.value_objects.entity_id import EntityId


class TicketRepositoryInterface(Protocol):
    async def get(self, id: EntityId) -> Ticket | None:
        raise NotImplementedError

    async def save_many(self, tickets: list[Ticket]) -> None:
        raise NotImplementedError

    async def all_unique_keys(self) -> set[TicketUniqueKey]:
        raise NotImplementedError
