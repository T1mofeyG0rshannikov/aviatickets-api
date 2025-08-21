from datetime import datetime

import httpx
import isodate

from src.entities.exceptions import FetchAPIError, InvalidParseParamsError
from src.entities.tickets.dto import CreateAviaTicketDTO, CreateTicketSegmentDTO
from src.infrastructure.clients.base_http_client import BaseHttpClient
from src.infrastructure.clients.retry_decorator import retry
from src.infrastructure.clients.ticket_parsers.amadeus.config import AmadeusAPIConfig
from src.infrastructure.repositories.airlline_repository import AirlineRepository
from src.infrastructure.repositories.airport_repository import AirportRepository
from src.interface_adapters.tickets_parser import TicketsParseParams, TicketsParser


class AmadeusTicketParser(TicketsParser, BaseHttpClient):
    def __init__(
        self,
        session: httpx.AsyncClient,
        config: AmadeusAPIConfig,
        repository: AirportRepository,
        airline_repository: AirlineRepository,
    ) -> None:
        super().__init__(session)
        self._config = config
        self.repository = repository
        self.airline_repository = airline_repository

    def format_date(self, date: datetime) -> str:
        return date.strftime("%Y-%m-%d")

    def iso_time_to_minutes(self, iso_time_string: str) -> int:
        try:
            duration = isodate.parse_duration(iso_time_string)
            total_seconds = duration.total_seconds()
            minutes = total_seconds / 60
            return minutes
        except isodate.ISO8601Error:
            return None

    async def build_dto(self, response_data: list[dict]) -> list[CreateAviaTicketDTO]:
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
            segments_dto = [
                CreateTicketSegmentDTO(
                    flight_number=segment["number"],
                    origin_airport_id=airports_dict[segment["departure"]["iataCode"]],
                    destination_airport_id=airports_dict[segment["arrival"]["iataCode"]],
                    airline_id=airlines_dict[segment["carrierCode"]],
                    departure_at=datetime.strptime(segment["departure"]["at"], "%Y-%m-%dT%H:%M:%S"),
                    return_at=datetime.strptime(segment["arrival"]["at"], "%Y-%m-%dT%H:%M:%S"),
                    duration=self.iso_time_to_minutes(segment["duration"]),
                )
                for segment in t["itineraries"][0]["segments"]
            ]

            dto_list.append(
                CreateAviaTicketDTO(
                    duration=self.iso_time_to_minutes(t["itineraries"][0]["duration"]),
                    price=float(t["price"]["total"]),
                    currency=t["price"]["currency"],
                    transfers=len(segments_dto) - 1,
                    segments=segments_dto,
                )
            )

        return dto_list

    @retry()
    async def get_access_token(self) -> str:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "client_credentials",
            "client_id": self._config.api_key,
            "client_secret": self._config.secret,
        }

        response = await self.session.post(self._config.oauth2_url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            raise FetchAPIError("Error getting access token: " + response.text)

    @retry()
    async def parse(self, params: TicketsParseParams) -> list[CreateAviaTicketDTO]:
        access_token = await self.get_access_token()

        params = {
            "originLocationCode": params.origin_airport.iata,
            "destinationLocationCode": params.destination_airport.iata,
            "departureDate": self.format_date(params.departure_at),
            "adults": params.adults,
            "children": params.childrens,
            "infants": params.infants,
            "returnDate": self.format_date(params.return_at),
        }

        headers = {"Authorization": f"Bearer {access_token}"}

        response = await self.session.get(self._config.url, headers=headers, params=params)
        print(response)
        print(response.json())

        if response.is_error:
            raise InvalidParseParamsError(response.json()["errors"][0]["detail"])

        json = response.json()

        return await self.build_dto(json["data"])
