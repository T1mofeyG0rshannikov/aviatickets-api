from datetime import datetime

from pydantic import BaseModel

from src.entities.tickets.filters import TicketsFilter


class ParseTicketsRequest(BaseModel):
    origin_airport_ids: list[int]
    destination_airport_ids: list[int]
    departure_at: datetime
    return_at: datetime
    adults: int = 1
    childrens: int = 0
    infants: int = 0


class FilterTicketsRequest(BaseModel, TicketsFilter):
    pass
