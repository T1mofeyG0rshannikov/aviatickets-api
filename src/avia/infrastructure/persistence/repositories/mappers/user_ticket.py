from avia.entities.user.value_objects.user_id import UserId
from avia.entities.user_ticket.user_ticket import UserTicket
from avia.entities.value_objects.entity_id import EntityId
from avia.infrastructure.persistence.db.models.models import UserTicketOrm
from avia.infrastructure.persistence.repositories.mappers.passengers import (
    from_orm_to_passenger,
)


def from_orm_to_user_ticket(user_ticket: UserTicketOrm) -> UserTicket:
    return UserTicket(
        id=EntityId(value=user_ticket.id),
        user_id=UserId(value=user_ticket.user_id),
        ticket_id=EntityId(user_ticket.ticket_id),
        passengers=[from_orm_to_passenger(passenger) for passenger in user_ticket.passengers],
    )
