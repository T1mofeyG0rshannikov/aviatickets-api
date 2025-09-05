from datetime import datetime
from decimal import Decimal

import isodate

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
from src.infrastructure.timezone_resolver import TimezoneResolver


class AmadeusTicketAdapter:
    def __init__(
        self, repository: AirportRepository, airline_repository: AirlineRepository, timezone_resolver: TimezoneResolver
    ) -> None:
        self.repository = repository
        self.airline_repository = airline_repository
        self.timezone_resolver = timezone_resolver

    def iso_time_to_minutes(self, iso_time_string: str) -> int:
        duration = isodate.parse_duration(iso_time_string)
        total_seconds = duration.total_seconds()
        minutes = total_seconds / 60
        return minutes

    def get_seat_class(self, raw_seat_class: str) -> str:
        class_codes = {
            SeatClassEnum.first: ["F", "P", "A"],
            SeatClassEnum.business: ["J", "C", "D", "I", "Z"],
            SeatClassEnum.premium_economy: ["W", "S"],
            SeatClassEnum.economy: ["Y", "B", "H", "K", "L", "M", "Q", "V", "T", "X", "E", "N", "O", "R"],
        }

        for class_name, class_codes in class_codes.items():  # type: ignore
            if raw_seat_class in class_codes:
                return class_name

        return SeatClassEnum.economy

    async def build(self, response_data: list[dict]) -> list[CreateTicketDTO]:
        dto_list = []
        airports_iata = set()
        airlines_iata = set()

        for t in response_data:
            for itinerary in t["itineraries"]:
                for segment in itinerary["segments"]:
                    airports_iata.add(segment["departure"]["iataCode"])
                    airports_iata.add(segment["arrival"]["iataCode"])
                    airlines_iata.add(segment["carrierCode"])

        airports = await self.repository.filter(iata_codes=airports_iata)
        airlines = await self.airline_repository.filter(iata_codes=airlines_iata)
        airports_dict = {airport.iata: airport for airport in airports}

        airlines_dict = {airline.iata: airline for airline in airlines}

        for t in response_data:
            itineraries_dto = []
            for itinerary in t["itineraries"]:
                segments_dto = []

                for ind, segment in enumerate(itinerary["segments"]):
                    try:
                        origin_airport = airports_dict[segment["departure"]["iataCode"]]
                    except KeyError:
                        print(f'''no airport with iata "{segment["departure"]["iataCode"]}"''')
                        continue

                    try:
                        destination_airport = airports_dict[segment["arrival"]["iataCode"]]
                    except KeyError:
                        print(f'''no airport with iata "{segment["arrival"]["iataCode"]}"''')
                        continue

                    departure_at = datetime.fromisoformat(segment["departure"]["at"]).replace(
                        tzinfo=self.timezone_resolver.get_timezone(origin_airport.iata)
                    )
                    arrival_at = datetime.fromisoformat(segment["arrival"]["at"]).replace(
                        tzinfo=self.timezone_resolver.get_timezone(destination_airport.iata)
                    )

                    segments_dto.append(
                        CreateTicketSegmentDTO(
                            flight_number=f"""{airlines_dict[segment["carrierCode"]].iata}-{segment["number"]}""",
                            segment_number=ind + 1,
                            origin_airport_id=origin_airport.id.value,
                            destination_airport_id=destination_airport.id.value,
                            airline_id=airlines_dict[segment["carrierCode"]].id.value,
                            departure_at=departure_at,
                            return_at=arrival_at,
                            duration=self.iso_time_to_minutes(segment["duration"]),
                            seat_class=self.get_seat_class(
                                t["travelerPricings"][0]["fareDetailsBySegment"][ind]["class"]
                            ),
                            status="confirmed",
                        )
                    )

                itineraries_dto.append(
                    CreateTicketItineraryDTO(
                        duration=self.iso_time_to_minutes(itinerary["duration"]), segments=segments_dto
                    )
                )

            dto_list.append(
                CreateTicketDTO(
                    price=Decimal(t["price"]["total"]),
                    currency=t["price"]["currency"],
                    itineraries=itineraries_dto,
                )
            )

        return dto_list
