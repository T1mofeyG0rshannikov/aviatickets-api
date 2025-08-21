from datetime import datetime

from src.entities.exceptions import AirportNotFoundError, FetchAPIError
from src.infrastructure.repositories.airport_repository import AirportRepository
from src.infrastructure.repositories.tickets_repository import TicketRepository
from src.interface_adapters.tickets_parser import TicketsParseParams, TicketsParser


class ParseAviaTickets:
    def __init__(
        self, parsers: list[TicketsParser], airports_repository: AirportRepository, ticket_repository: TicketRepository
    ) -> None:
        self._parsers = parsers
        self.airports_repository = airports_repository
        self.ticket_repository = ticket_repository

    async def get_exist_tickets_hashes(self) -> list[str]:
        exist_tickets = await self.ticket_repository.all()
        return {hash(segment.flight_number for segment in ticket.segments) for ticket in exist_tickets}

    async def __call__(
        self,
        origin_airport_ids: list[int],
        destination_airport_ids: list[int],
        departure_at: datetime,
        return_at: datetime,
        adults: int,
        childrens: int,
        infants: int,
    ) -> None:
        parsed_tickets = set()

        for origin_airport_id in origin_airport_ids:
            for destination_airport_id in destination_airport_ids:
                origin_airport = await self.airports_repository.get(id=origin_airport_id)
                if origin_airport is None:
                    raise AirportNotFoundError(f"no airport with id = {origin_airport_id} found")

                destination_airport = await self.airports_repository.get(id=destination_airport_id)
                if destination_airport is None:
                    raise AirportNotFoundError(f"no airport with id = {destination_airport_id} found")

                for parser in self._parsers:
                    try:
                        tickets = await parser.parse(
                            TicketsParseParams(
                                origin_airport=origin_airport,
                                destination_airport=destination_airport,
                                departure_at=departure_at,
                                return_at=return_at,
                                adults=adults,
                                childrens=childrens,
                                infants=infants,
                            )
                        )

                        parsed_tickets.update(tickets)
                    except FetchAPIError as e:
                        print(f"Error while fetcing tickets {e}")

        exist_tickets_hashes = await self.get_exist_tickets_hashes()

        tickets_to_create = [ticket for ticket in parsed_tickets if hash(ticket) not in exist_tickets_hashes]

        return await self.ticket_repository.create_many(tickets_to_create)
