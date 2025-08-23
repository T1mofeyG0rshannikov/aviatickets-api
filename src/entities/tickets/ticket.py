from dataclasses import dataclass
from datetime import datetime

from src.entities.value_objects.entity_id import EntityId


@dataclass
class TicketSegment:
    id: EntityId
    segment_number: int
    flight_number: int
    origin_airport_id: EntityId
    destination_airport_id: EntityId
    airline_id: EntityId
    departure_at: datetime
    return_at: datetime
    duration: int
    seat_class: str
    status: str

    @classmethod
    def create(
        cls,
        flight_number: int,
        segment_number: int,
        origin_airport_id: EntityId,
        destination_airport_id: EntityId,
        airline_id: EntityId,
        departure_at: datetime,
        return_at: datetime,
        duration: int,
        seat_class: str,
        status: str,
    ):
        return cls(
            id=EntityId.generate(),
            flight_number=flight_number,
            segment_number=segment_number,
            origin_airport_id=origin_airport_id,
            destination_airport_id=destination_airport_id,
            airline_id=airline_id,
            departure_at=departure_at,
            return_at=return_at,
            duration=duration,
            seat_class=seat_class,
            status=status,
        )


@dataclass
class Ticket:
    id: EntityId
    duration: int
    price: int
    currency: str
    transfers: int
    segments: list[TicketSegment]

    @classmethod
    def create(cls, duration: int, price: int, currency: str, transfers: int, segments: list[TicketSegment]):
        return cls(
            id=EntityId.generate(),
            duration=duration,
            price=price,
            currency=currency,
            transfers=transfers,
            segments=segments,
        )
