from src.entities.user_ticket.user_ticket import UserTicket
from src.infrastructure.db.models.models import UserTicketOrm


def from_orm_to_user_ticket(user_ticket: UserTicketOrm) -> UserTicket:
    return UserTicket(id=user_ticket.id, user_id=user_ticket.user_id, ticket_id=user_ticket.ticket_id)
