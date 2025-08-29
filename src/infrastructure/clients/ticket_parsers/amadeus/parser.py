from datetime import datetime

import httpx

from src.application.dto.ticket import CreateTicketDTO
from src.infrastructure.clients.base_http_client import BaseHttpClient
from src.infrastructure.clients.retry_decorator import retry
from src.infrastructure.clients.ticket_parsers.amadeus.adapter import (
    AmadeusTicketAdapter,
)
from src.infrastructure.clients.ticket_parsers.amadeus.config import AmadeusAPIConfig
from src.infrastructure.exceptions import FetchAPIError, InvalidParseParamsError
from src.infrastructure.persistence.repositories.airport_repository import (
    AirportRepository,
)
from src.interface_adapters.tickets_parser import TicketsParseParams, TicketsParser


class AmadeusTicketParser(TicketsParser, BaseHttpClient):
    def __init__(
        self,
        session: httpx.AsyncClient,
        config: AmadeusAPIConfig,
        repository: AirportRepository,
        adapter: AmadeusTicketAdapter,
    ) -> None:
        super().__init__(session)
        self._config = config
        self.repository = repository
        self.builder = adapter

    def format_date(self, date: datetime) -> str:
        return date.strftime("%Y-%m-%d")

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
    async def parse(self, params: TicketsParseParams) -> list[CreateTicketDTO]:
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

        return await self.builder.build(json["data"])
