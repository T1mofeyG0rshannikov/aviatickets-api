from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from src.application.dto.airline import AirlineDTO
from src.application.dto.airports.full_info import AirportFullInfoDTO


@dataclass
class TicketSegmentFullInfoDTO:
    id: UUID
    flight_number: str
    segment_number: int
    destination_airport: AirportFullInfoDTO
    origin_airport: AirportFullInfoDTO
    airline: AirlineDTO
    departure_at: datetime
    return_at: datetime
    duration: int
    status: str
    seat_class: str


@dataclass
class TicketFullInfoDTO:
    id: UUID
    duration: int
    price: Decimal
    currency: str
    transfers: int
    segments: list[TicketSegmentFullInfoDTO]


class CreateTicketSegmentDTO(BaseModel):
    flight_number: str
    segment_number: int
    origin_airport_id: UUID
    destination_airport_id: UUID
    airline_id: UUID
    departure_at: datetime
    return_at: datetime
    duration: int
    seat_class: str
    status: str


class CreateTicketDTO(BaseModel):
    currency: str
    duration: int
    price: Decimal
    transfers: int
    segments: list[CreateTicketSegmentDTO]
