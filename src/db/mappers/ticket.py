from src.db.models.models import TicketOrm
from src.entities.tickets.ticket import Ticket


def orm_to_ticket(ticket: TicketOrm) -> Ticket:
    return Ticket(
        id=ticket.id,
        origin_airport_id=ticket.origin_airport_id,
        destination_airport_id=ticket.destination_airport_id,
        airline_id=ticket.airline_id,
        departure_at=ticket.departure_at,
        return_at=ticket.return_at,
        duration=ticket.duration,
        price=ticket.price,
        transfers=ticket.transfers,
    )
