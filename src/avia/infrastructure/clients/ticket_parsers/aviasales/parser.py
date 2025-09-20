from datetime import datetime

import httpx

from avia.application.dto.ticket import CreateTicketDTO
from avia.application.exceptions import FetchAPIError
from avia.application.tickets_parser import TicketsParseParams, TicketsParser
from avia.infrastructure.clients.base_http_client import BaseHttpClient
from avia.infrastructure.clients.retry_decorator import retry
from avia.infrastructure.clients.ticket_parsers.aviasales.adapter import (
    AviasalesTicketAdapter,
)
from avia.infrastructure.clients.ticket_parsers.aviasales.config import (
    AviasalesAPIConfig,
)
from avia.infrastructure.persistence.repositories.airport_repository import (
    AirportRepository,
)


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
    async def parse(self, params: TicketsParseParams) -> list[CreateTicketDTO]:
        url_params = {
            "origin": params.origin_airport.iata,
            "destination": params.destination_airport.iata,
            "departure_at": self.format_date(params.departure_at),
            "return_at": self.format_date(params.return_at),
            "token": self._config.api_token,
            "adults": params.adults,
            "children": params.childrens,
            "infants": params.infants,
            "one_way": False,
            "transfers": 0,
        }

        response = await self.session.get(self._config.url, params=url_params)
        if response.is_error:
            raise FetchAPIError("error while fetching aviasales api")

        json = response.json()

        return await self.adapter.build(json["data"])
