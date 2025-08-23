from datetime import datetime

import isodate

from src.entities.tickets.ticket import Ticket, TicketSegment
from src.infrastructure.persistence.repositories.airlline_repository import (
    AirlineRepository,
)
from src.infrastructure.persistence.repositories.airport_repository import (
    AirportRepository,
)


class AmadeusTicketAdapter:
    def __init__(
        self,
        repository: AirportRepository,
        airline_repository: AirlineRepository,
    ) -> None:
        self.repository = repository
        self.airline_repository = airline_repository

    def iso_time_to_minutes(self, iso_time_string: str) -> int:
        try:
            duration = isodate.parse_duration(iso_time_string)
            total_seconds = duration.total_seconds()
            minutes = total_seconds / 60
            return minutes
        except isodate.ISO8601Error:
            return None

    def get_seat_class(self, raw_seat_class: str) -> str:
        class_codes = {
            "first": ["F", "P", "A"],
            "business": ["J", "C", "D", "I", "Z"],
            "premium economy": ["W", "S"],
            "economy": ["Y", "B", "H", "K", "L", "M", "Q", "V", "T", "X", "E", "N", "O", "R"],
        }

        for class_name, class_codes in class_codes.items():
            if raw_seat_class in class_codes:
                return class_name

    async def build(self, response_data: list[dict]) -> list[Ticket]:
        dto_list = []
        airports_iata = set()
        airlines_iata = set()

        for t in response_data:
            for segment in t["itineraries"][0]["segments"]:
                airports_iata.add(segment["departure"]["iataCode"])
                airports_iata.add(segment["arrival"]["iataCode"])
                airlines_iata.add(segment["carrierCode"])

        airports = await self.repository.filter(iata_codes=airports_iata)
        airlines = await self.airline_repository.filter(iata_codes=airlines_iata)
        airports_dict = {airport.iata: airport.id for airport in airports}

        airlines_dict = {airline.iata: airline.id for airline in airlines}

        for t in response_data:
            segments_dto = []
            for ind, segment in enumerate(t["itineraries"][0]["segments"]):
                # print(t["travelerPricings"][ind])
                segments_dto.append(
                    TicketSegment.create(
                        flight_number=segment["number"],
                        segment_number=ind + 1,
                        origin_airport_id=airports_dict[segment["departure"]["iataCode"]],
                        destination_airport_id=airports_dict[segment["arrival"]["iataCode"]],
                        airline_id=airlines_dict[segment["carrierCode"]],
                        departure_at=datetime.strptime(segment["departure"]["at"], "%Y-%m-%dT%H:%M:%S"),
                        return_at=datetime.strptime(segment["arrival"]["at"], "%Y-%m-%dT%H:%M:%S"),
                        duration=self.iso_time_to_minutes(segment["duration"]),
                        seat_class=self.get_seat_class(t["travelerPricings"][0]["fareDetailsBySegment"][ind]["class"]),
                        status="confirmed",
                    )
                )

            dto_list.append(
                Ticket.create(
                    duration=self.iso_time_to_minutes(t["itineraries"][0]["duration"]),
                    price=float(t["price"]["total"]),
                    currency=t["price"]["currency"],
                    transfers=len(segments_dto) - 1,
                    segments=segments_dto,
                )
            )

        return dto_list
