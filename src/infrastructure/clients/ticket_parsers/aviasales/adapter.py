from datetime import datetime

from src.entities.tickets.ticket import Ticket, TicketSegment
from src.infrastructure.clients.ticket_parsers.aviasales.config import (
    AviasalesAPIConfig,
)
from src.infrastructure.persistence.repositories.airlline_repository import (
    AirlineRepository,
)
from src.infrastructure.persistence.repositories.airport_repository import (
    AirportRepository,
)


class AviasalesTicketAdapter:
    def __init__(
        self,
        repository: AirportRepository,
        airline_repository: AirlineRepository,
    ) -> None:
        self.repository = repository
        self.airline_repository = airline_repository

    async def build(self, response_data: list[dict]) -> list[Ticket]:
        dto_list = []
        airports_iata = set()
        airlines_iata = set()

        for t in response_data:
            airports_iata.add(t["origin_airport"])
            airports_iata.add(t["destination_airport"])
            airlines_iata.add(t["airline"])

        airports = await self.repository.filter(iata_codes=airports_iata)
        airlines = await self.airline_repository.filter(iata_codes=airlines_iata)
        airports_dict = {airport.iata: airport.id for airport in airports}

        airlines_dict = {airline.iata: airline.id for airline in airlines}

        for t in response_data:
            if t["transfers"] == 0:
                segments_dto = [
                    TicketSegment.create(
                        flight_number=t["flight_number"],
                        segment_number=1,
                        origin_airport_id=airports_dict[t["origin_airport"]],
                        destination_airport_id=airports_dict[t["destination_airport"]],
                        airline_id=airlines_dict[t["airline"]],
                        departure_at=datetime.fromisoformat(t["departure_at"]),
                        return_at=datetime.fromisoformat(t["return_at"]),
                        duration=t["duration"],
                        seat_class="economy",
                        status="confirmed",
                    )
                ]

                dto_list.append(
                    Ticket.create(
                        currency="RUB",
                        segments=segments_dto,
                        duration=t["duration"],
                        price=t["price"],
                        transfers=t["transfers"],
                    )
                )

        return dto_list
