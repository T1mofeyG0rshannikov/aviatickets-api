from datetime import datetime

import httpx

from src.entities.exceptions import FetchAPIError
from src.entities.tickets.dto import CreateAviaTicketDTO, CreateTicketSegmentDTO
from src.infrastructure.clients.base_http_client import BaseHttpClient
from src.infrastructure.clients.retry_decorator import retry
from src.infrastructure.clients.ticket_parsers.aviasales.config import (
    AviasalesAPIConfig,
)
from src.infrastructure.repositories.airlline_repository import AirlineRepository
from src.infrastructure.repositories.airport_repository import AirportRepository
from src.interface_adapters.tickets_parser import TicketsParseParams, TicketsParser


class AviasalesTicketParser(TicketsParser, BaseHttpClient):
    def __init__(
        self,
        session: httpx.AsyncClient,
        config: AviasalesAPIConfig,
        repository: AirportRepository,
        airline_repository: AirlineRepository,
    ) -> None:
        super().__init__(session)
        self._config = config
        self.repository = repository
        self.airline_repository = airline_repository

    def format_date(self, date: datetime) -> str:
        return date.strftime("%Y-%m")

    async def build_dto(self, response_data: list[dict]) -> list[CreateAviaTicketDTO]:
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
            segments_dto = [
                CreateTicketSegmentDTO(
                    flight_number=t["flight_number"],
                    origin_airport_id=airports_dict[t["origin_airport"]],
                    destination_airport_id=airports_dict["destination_airport"],
                    airline_id=airlines_dict[t["airline"]],
                    departure_at=datetime.fromisoformat(t["departure_at"]),
                    return_at=datetime.fromisoformat(t["return_at"]),
                    duration=t["duration"],
                )
            ]

            dto_list.append(
                CreateAviaTicketDTO(
                    currency="RUB",
                    segments=segments_dto,
                    duration=t["duration"],
                    price=t["price"],
                    transfers=t["transfers"],
                )
            )

        return dto_list

    @retry()
    async def parse(self, params: TicketsParseParams) -> list[CreateAviaTicketDTO]:
        params = {
            "origin": params.origin_airport.iata,
            "destination": params.destination_airport.iata,
            "departure_at": self.format_date(params.departure_at),
            "return_at": self.format_date(params.return_at),
            "one_way": "true",
            "token": self._config.api_token,
            "adults": params.adults,
            "children": params.childrens,
            "infants": params.infants,
            "transfers": 0,
        }

        response = await self.session.get(self._config.url, params=params)
        print(response)
        print(response.json())
        if response.is_error:
            raise FetchAPIError("error while fetching aviasales api")

        json = response.json()

        print(json)

        return await self.build_dto(json["data"])
