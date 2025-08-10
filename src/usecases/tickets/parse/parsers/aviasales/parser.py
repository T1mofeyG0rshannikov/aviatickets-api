from datetime import datetime
from typing import List

import httpx

from src.dto.ticket import CreateAviaTicketDTO
from src.entities.airport.airport import Airport
from src.entities.exceptions import FetchAPIException
from src.repositories.airlline_repository import AirlineRepository
from src.repositories.airport_repository import AirportRepository
from src.usecases.tickets.parse.parsers.aviasales.config import AviasalesAPIConfig
from src.usecases.tickets.parse.parsers.base import TicketsParser


class AviasalesTicketParser(TicketsParser):
    def __init__(
        self, config: AviasalesAPIConfig, repository: AirportRepository, airline_repository: AirlineRepository
    ) -> None:
        self._config = config
        self.repository = repository
        self.airline_repository = airline_repository

    def format_date(self, date: datetime) -> str:
        return date.strftime("%Y-%m")

    async def build_dto(self, response_data: list[dict]) -> list[CreateAviaTicketDTO]:
        dto_list = []
        for t in response_data:
            origin_airport = await self.repository.get(iata=t["origin_airport"])
            destilation_airport = await self.repository.get(iata=t["destination_airport"])
            airline = await self.airline_repository.get(iata=t["airline"])

            dto_list.append(
                CreateAviaTicketDTO(
                    origin_airport_id=origin_airport.id,
                    destination_airport_id=destilation_airport.id,
                    airline_id=airline.id,
                    departure_at=datetime.strptime(t["departure_at"], "%Y-%m-%dT%H:%M:%S%z"),
                    return_at=datetime.strptime(t["return_at"], "%Y-%m-%dT%H:%M:%S%z"),
                    duration=t["duration"],
                    price=t["price"],
                    transfers=t["transfers"],
                )
            )

        return dto_list

    async def parse(
        self, origin_airport: Airport, destination_airport: Airport, departure_at: datetime, return_at: datetime
    ) -> list[CreateAviaTicketDTO]:
        async with httpx.AsyncClient() as session:
            params = {
                "origin": origin_airport.iata,
                "destination": destination_airport.iata,
                "departure_at": self.format_date(departure_at),
                "return_at": self.format_date(return_at),
                "currency": "rub",
                "one_way": "true",
                "token": self._config.api_token,
            }

            response = await session.get(self._config.url, params=params)

            if response.is_error:
                raise FetchAPIException("error while fetching aviasales api")

            json = response.json()

            print(json)

            return await self.build_dto(json["data"])
