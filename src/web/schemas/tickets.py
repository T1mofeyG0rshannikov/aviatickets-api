from datetime import datetime
from typing import List

from pydantic import BaseModel

from src.entities.tickets.filters import TicketsFilter


class ParseTicketsRequest(BaseModel):
    origin_airport_ids: list[int]
    destination_airport_ids: list[int]
    departure_at: datetime
    return_at: datetime


class FilterTicketsRequest(BaseModel, TicketsFilter):
    pass


class AirportResponse(BaseModel):
    id: int
    name: str
    continent: str
    country_id: int
    region_id: int
    city_id: int
    scheduled_service: str
    icao: str
    iata: str
    gps_code: str
    name_russian: str = None


class AirlineResponse(BaseModel):
    id: int
    iata: str
    icao: str
    name: str
    name_russian: str


class TicketFullInfoResponse(BaseModel):
    id: int
    origin_airport: AirportResponse
    destination_airport: AirportResponse
    airline: AirlineResponse
    departure_at: datetime
    return_at: datetime
    duration: int
    price: int
    transfers: int
