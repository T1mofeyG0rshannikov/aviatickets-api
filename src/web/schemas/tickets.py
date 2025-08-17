from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.entities.tickets.filters import TicketsFilter


class ParseTicketsRequest(BaseModel):
    origin_airport_ids: list[int]
    destination_airport_ids: list[int]
    departure_at: datetime
    return_at: datetime


class FilterTicketsRequest(BaseModel, TicketsFilter):
    pass


class CountryResponse(BaseModel):
    id: int
    iso: str
    name: str
    name_english: str


class RegionResponse(BaseModel):
    id: int
    iso: str
    name: str
    name_english: str


class CityResponse(BaseModel):
    id: int
    name: str
    name_english: str


class AirportFullInfoResponse(BaseModel):
    id: int
    name: str
    continent: str
    scheduled_service: str
    icao: str
    iata: str
    gps_code: str
    country: CountryResponse | None = None
    region: RegionResponse | None = None
    city: CityResponse | None = None
    name_russian: str | None = None


class AirlineResponse(BaseModel):
    id: int
    iata: str
    icao: str
    name: str
    name_russian: str


class TicketFullInfoResponse(BaseModel):
    id: int
    origin_airport: AirportFullInfoResponse
    destination_airport: AirportFullInfoResponse
    airline: AirlineResponse
    departure_at: datetime
    return_at: datetime
    duration: int
    price: int
    transfers: int
