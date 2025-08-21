from src.entities.tickets.ticket import Ticket, TicketSegment
from src.infrastructure.db.models.models import TicketOrm, TicketSegmentOrm


def orm_to_ticket_segment(segment: TicketSegmentOrm) -> TicketSegment:
    return TicketSegment(
        id=segment.id,
        flight_number=segment.flight_number,
        origin_airport_id=segment.origin_airport_id,
        destination_airport_id=segment.destination_airport_id,
        airline_id=segment.airline_id,
        departure_at=segment.departure_at,
        return_at=segment.return_at,
        duration=segment.duration,
        seat_class=segment.seat_class,
        status=segment.status,
    )


def orm_to_ticket(ticket: TicketOrm) -> Ticket:
    return Ticket(
        id=ticket.id,
        duration=ticket.duration,
        price=ticket.price,
        transfers=ticket.transfers,
        currency=ticket.currency,
        segments=[orm_to_ticket_segment(segment) for segment in ticket.segments],
    )
