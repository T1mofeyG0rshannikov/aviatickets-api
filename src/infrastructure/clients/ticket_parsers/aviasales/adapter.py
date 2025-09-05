from datetime import datetime

from src.application.dto.ticket import (
    CreateTicketDTO,
    CreateTicketItineraryDTO,
    CreateTicketSegmentDTO,
)
from src.entities.tickets.value_objects.seat_class.enum import SeatClassEnum
from src.infrastructure.persistence.repositories.airline_repository import (
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

    async def build(self, response_data: list[dict]) -> list[CreateTicketDTO]:
        dto_list = []
        airports_iata = set()
        airlines_iata = set()

        for t in response_data:
            airports_iata.add(t["origin_airport"])
            airports_iata.add(t["destination_airport"])
            airlines_iata.add(t["airline"])

        airports = await self.repository.filter(iata_codes=airports_iata)
        airlines = await self.airline_repository.filter(iata_codes=airlines_iata)
        airports_dict = {airport.iata: airport.id.value for airport in airports}

        airlines_dict = {airline.iata: airline for airline in airlines}

        for t in response_data:
            if t["transfers"] == 0:
                segments_dto = [
                    CreateTicketSegmentDTO(
                        flight_number=f"""{airlines_dict[t["airline"]].iata}-{t["flight_number"]}""",
                        segment_number=1,
                        origin_airport_id=airports_dict[t["origin_airport"]],
                        destination_airport_id=airports_dict[t["destination_airport"]],
                        airline_id=airlines_dict[t["airline"]].id.value,
                        departure_at=datetime.fromisoformat(t["departure_at"]),
                        return_at=datetime.fromisoformat(t["return_at"]),
                        duration=t["duration"],
                        seat_class=SeatClassEnum.economy,
                        status="confirmed",
                    )
                ]

                itineraries_dto = [CreateTicketItineraryDTO(segments=segments_dto, duration=t["duration"])]

                dto_list.append(
                    CreateTicketDTO(
                        currency="RUB",
                        itineraries=itineraries_dto,
                        price=t["price"],
                    )
                )

        return dto_list
