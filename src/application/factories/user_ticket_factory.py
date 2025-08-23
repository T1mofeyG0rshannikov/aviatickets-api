from uuid import UUID

from src.entities.user_ticket.user_ticket import UserTicket
from src.entities.value_objects.entity_id import EntityId


class UserTicketFactory:
    @classmethod
    def create(cls, user_id: UUID, ticket_id: UUID) -> UserTicket:
        return UserTicket.create(user_id=EntityId(user_id), ticket_id=EntityId(ticket_id))
