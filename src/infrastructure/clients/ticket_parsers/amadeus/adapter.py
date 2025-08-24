from datetime import datetime
from zoneinfo import ZoneInfo

import isodate

from src.application.factories.ticket_segment_factory import TicketSegmentFactory
from src.entities.tickets.ticket import Ticket
from src.infrastructure.persistence.repositories.airlline_repository import (
    AirlineRepository,
)
from src.infrastructure.persistence.repositories.airport_repository import (
    AirportRepository,
)
from src.infrastructure.timezone_resolver import TimezoneResolver


class AmadeusTicketAdapter:
    def __init__(
        self, repository: AirportRepository, airline_repository: AirlineRepository, timezone_resolver: TimezoneResolver
    ) -> None:
        self.repository = repository
        self.airline_repository = airline_repository
        self.timezone_resolver = timezone_resolver

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
        airports_dict = {airport.iata: airport for airport in airports}

        airlines_dict = {airline.iata: airline for airline in airlines}

        for t in response_data:
            segments_dto = []
            for ind, segment in enumerate(t["itineraries"][0]["segments"]):
                origin_airport = airports_dict[segment["departure"]["iataCode"]]
                destination_airport = airports_dict[segment["arrival"]["iataCode"]]

                departure_at = datetime.fromisoformat(segment["departure"]["at"]).replace(
                    tzinfo=self.timezone_resolver.get_timezone(origin_airport.iata)
                )
                arrival_at = datetime.fromisoformat(segment["arrival"]["at"]).replace(
                    tzinfo=self.timezone_resolver.get_timezone(destination_airport.iata)
                )

                departure_at = self.timezone_resolver(segment["departure"]["at"])
                segments_dto.append(
                    TicketSegmentFactory.create(
                        flight_number=f"""{airlines_dict[segment["carrierCode"]].iata}-{segment["number"]}""",
                        segment_number=ind + 1,
                        origin_airport_id=origin_airport.id.value,
                        destination_airport_id=destination_airport.id.value,
                        airline_id=airlines_dict[segment["carrierCode"]].id.value,
                        departure_at=departure_at,
                        return_at=arrival_at,
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
