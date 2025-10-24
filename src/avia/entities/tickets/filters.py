from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class TicketsFilter:
    price_min: int | None = None
    price_max: int | None = None
    airline_ids: list[UUID] | None = None
    origin_airport_ids: list[UUID] | None = None
    destination_airport_ids: list[UUID] | None = None
    duration_min: int | None = None
    duration_max: int | None = None
    transfers: list[int] | None = None
    departure_at: datetime | None = None
    departure_at_time_min: int = 0  # in minutes
    departure_at_time_max: int = 24 * 60 - 1  # in minutes
    return_at: datetime | None = None
    return_at_time_min: int = 0  # in minutes
    return_at_time_max: int = 24 * 60 - 1  # in minutes
