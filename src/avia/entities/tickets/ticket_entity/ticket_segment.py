from dataclasses import dataclass

import pytz  # type: ignore

from avia.entities.airport.airport import Airport
from avia.entities.tickets.exceptions import DepartureAtMustBeBeforeReturnAtError
from avia.entities.tickets.value_objects.departure_at import DepartureAt
from avia.entities.tickets.value_objects.flight_number import FlightNumber
from avia.entities.tickets.value_objects.return_at import ReturnAt
from avia.entities.value_objects.entity_id import EntityId


@dataclass
class TicketSegment:
    id: EntityId
    segment_number: int
    flight_number: FlightNumber
    origin_airport: Airport
    destination_airport: Airport
    airline_id: EntityId
    departure_at: DepartureAt
    return_at: ReturnAt
    duration: int
    seat_class: str
    status: str
    aircraft_id: EntityId

    @classmethod
    def create(
        cls,
        flight_number: FlightNumber,
        segment_number: int,
        origin_airport: Airport,
        destination_airport: Airport,
        airline_id: EntityId,
        aircraft_id: EntityId,
        departure_at: DepartureAt,
        return_at: ReturnAt,
        duration: int,
        seat_class: str,
        status: str,
    ):
        utc_departure_at = departure_at.value.astimezone(pytz.utc)
        utc_return_at = return_at.value.astimezone(pytz.utc)

        if utc_return_at < utc_departure_at:
            raise DepartureAtMustBeBeforeReturnAtError("departure at must be before return at")

        return cls(
            id=EntityId.generate(),
            flight_number=flight_number,
            segment_number=segment_number,
            origin_airport=origin_airport,
            destination_airport=destination_airport,
            airline_id=airline_id,
            departure_at=departure_at,
            return_at=return_at,
            duration=duration,
            seat_class=seat_class,
            aircraft_id=aircraft_id,
            status=status,
        )
