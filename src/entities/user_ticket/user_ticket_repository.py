from typing import Protocol

from src.entities.user_ticket.user_ticket import Passenger, UserTicket
from src.entities.value_objects.entity_id import EntityId


class UserTicketRepositoryInterface(Protocol):
    async def get_by_user_and_ticket_ids(self, user_id: EntityId, ticket_id: EntityId) -> UserTicket:
        raise NotImplementedError

    async def get(self, id: EntityId) -> UserTicket:
        raise NotImplementedError

    async def get_passangers(self, user_ticket_id: EntityId) -> list[Passenger]:
        raise NotImplementedError

    async def save(self, user_id: int, ticket_id: EntityId, passengers: list[Passenger]) -> UserTicket:
        raise NotImplementedError
