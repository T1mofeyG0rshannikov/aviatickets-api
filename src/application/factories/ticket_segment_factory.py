from datetime import datetime
from uuid import UUID

from src.entities.tickets.ticket import TicketSegment
from src.entities.tickets.value_objects.departure_at import DepartureAt
from src.entities.tickets.value_objects.flight_number import FlightNumber
from src.entities.tickets.value_objects.return_at import ReturnAt
from src.entities.value_objects.entity_id import EntityId


class TicketSegmentFactory:
    @classmethod
    def create(
        cls,
        flight_number: str,
        segment_number: int,
        origin_airport_id: UUID,
        destination_airport_id: UUID,
        airline_id: UUID,
        departure_at: datetime,
        return_at: datetime,
        duration: int,
        seat_class: str,
        status: str,
    ) -> TicketSegment:
        return TicketSegment.create(
            flight_number=FlightNumber(flight_number),
            segment_number=segment_number,
            origin_airport_id=EntityId(origin_airport_id),
            destination_airport_id=EntityId(destination_airport_id),
            airline_id=EntityId(airline_id),
            departure_at=DepartureAt(departure_at),
            return_at=ReturnAt(return_at),
            duration=duration,
            seat_class=seat_class,
            status=status,
        )
