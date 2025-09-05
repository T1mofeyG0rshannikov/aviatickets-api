from src.entities.tickets.ticket_entity.ticket import Ticket
from src.entities.tickets.ticket_entity.ticket_itinerary import TicketItinerary
from src.entities.tickets.ticket_entity.ticket_segment import TicketSegment
from src.entities.tickets.value_objects.flight_number import FlightNumber
from src.entities.tickets.value_objects.unique_key import TicketUniqueKey
from src.entities.value_objects.entity_id import EntityId
from src.entities.value_objects.price.price import Price
from src.infrastructure.persistence.db.models.models import (
    TicketItineraryOrm,
    TicketOrm,
    TicketSegmentOrm,
)


def orm_to_ticket_segment(segment: TicketSegmentOrm) -> TicketSegment:
    return TicketSegment(
        id=EntityId(segment.id),
        flight_number=FlightNumber(segment.flight_number),
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


def orm_to_itinerary(itinerary: TicketItineraryOrm) -> TicketItinerary:
    return TicketItinerary(
        id=EntityId(itinerary.id),
        transfers=itinerary.transfers,
        segments=[orm_to_ticket_segment(segment) for segment in itinerary.segments],
        duration=itinerary.duration,
    )


def orm_to_ticket(ticket: TicketOrm) -> Ticket:
    return Ticket(
        id=EntityId(ticket.id),
        unique_key=TicketUniqueKey(ticket.unique_key),
        price=Price(value=ticket.price, currency=ticket.currency),
        itineraries=[orm_to_itinerary(itinerary) for itinerary in ticket.itineraries],
    )
