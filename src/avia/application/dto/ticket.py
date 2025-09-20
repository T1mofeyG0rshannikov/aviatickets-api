from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from avia.application.dto.aircraft import AircraftDTO
from avia.application.dto.airline import AirlineDTO
from avia.application.dto.airports.full_info import AirportFullInfoDTO
from avia.entities.value_objects.price.currency_enum import CurrencyEnum


@dataclass
class TicketSegmentFullInfoDTO:
    flight_number: str
    segment_number: int
    destination_airport: AirportFullInfoDTO
    origin_airport: AirportFullInfoDTO
    airline: AirlineDTO
    aircraft: AircraftDTO
    departure_at: datetime
    return_at: datetime
    duration: int
    status: str
    seat_class: str


@dataclass
class TicketItineraryFullInfoDTO:
    transfers: int
    segments: list[TicketSegmentFullInfoDTO]
    duration: int


@dataclass
class TicketFullInfoDTO:
    id: UUID
    price: Decimal
    currency: CurrencyEnum
    itineraries: list[TicketItineraryFullInfoDTO]


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
    aircraft_id: UUID


class CreateTicketItineraryDTO(BaseModel):
    segments: list[CreateTicketSegmentDTO]
    duration: int


class CreateTicketDTO(BaseModel):
    currency: CurrencyEnum
    price: Decimal
    itineraries: list[CreateTicketItineraryDTO]
