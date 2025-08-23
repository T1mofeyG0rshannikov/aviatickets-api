from datetime import datetime

import httpx

from src.entities.tickets.ticket import Ticket
from src.infrastructure.clients.base_http_client import BaseHttpClient
from src.infrastructure.clients.retry_decorator import retry
from src.infrastructure.clients.ticket_parsers.aviasales.adapter import (
    AviasalesTicketAdapter,
)
from src.infrastructure.clients.ticket_parsers.aviasales.config import (
    AviasalesAPIConfig,
)
from src.infrastructure.exceptions import FetchAPIError
from src.infrastructure.persistence.repositories.airport_repository import (
    AirportRepository,
)
from src.interface_adapters.tickets_parser import TicketsParseParams, TicketsParser


class AviasalesTicketParser(TicketsParser, BaseHttpClient):
    def __init__(
        self,
        session: httpx.AsyncClient,
        config: AviasalesAPIConfig,
        repository: AirportRepository,
        adapter: AviasalesTicketAdapter,
    ) -> None:
        super().__init__(session)
        self._config = config
        self.repository = repository
        self.adapter = adapter

    def format_date(self, date: datetime) -> str:
        return date.strftime("%Y-%m")

    @retry()
    async def parse(self, params: TicketsParseParams) -> list[Ticket]:
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

        return await self.adapter.build(json["data"])
