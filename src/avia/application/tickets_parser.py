from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from avia.application.dto.ticket import CreateTicketDTO
from avia.entities.airport.airport import Airport


@dataclass
class TicketsParseParams:
    origin_airport: Airport
    destination_airport: Airport
    departure_at: datetime
    return_at: datetime
    adults: int
    childrens: int
    infants: int


class TicketsParser(ABC):
    @abstractmethod
    async def parse(self, params: TicketsParseParams) -> list[CreateTicketDTO]:
        ...
