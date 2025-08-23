from src.entities.tickets.ticket import Ticket, TicketSegment
from src.entities.value_objects.entity_id import EntityId
from src.infrastructure.persistence.db.models.models import TicketOrm, TicketSegmentOrm


def orm_to_ticket_segment(segment: TicketSegmentOrm) -> TicketSegment:
    return TicketSegment(
        id=EntityId(segment.id),
        flight_number=segment.flight_number,
        segment_number=segment.segment_number,
        origin_airport_id=EntityId(segment.origin_airport_id),
        destination_airport_id=EntityId(segment.destination_airport_id),
        airline_id=EntityId(segment.airline_id),
        departure_at=segment.departure_at,
        return_at=segment.return_at,
        duration=segment.duration,
        seat_class=segment.seat_class,
        status=segment.status,
    )


def orm_to_ticket(ticket: TicketOrm) -> Ticket:
    return Ticket(
        id=EntityId(ticket.id),
        duration=ticket.duration,
        price=ticket.price,
        transfers=ticket.transfers,
        currency=ticket.currency,
        segments=[orm_to_ticket_segment(segment) for segment in ticket.segments],
    )
