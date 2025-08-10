from abc import abstractmethod
from datetime import datetime
from typing import List

from src.dto.ticket import CreateAviaTicketDTO
from src.entities.airport.airport import Airport


class TicketsParser:
    @abstractmethod
    async def parse(
        self, origin_airport: Airport, destination_airport: Airport, departure_at: datetime, return_at: datetime
    ) -> list[CreateAviaTicketDTO]:
        ...
