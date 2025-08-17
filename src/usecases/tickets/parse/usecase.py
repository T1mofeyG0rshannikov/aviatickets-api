from datetime import datetime

from src.dto.ticket import CreateAviaTicketDTO
from src.entities.exceptions import AirportNotFoundException, FetchAPIException
from src.infrastructure.repositories.airport_repository import AirportRepository
from src.infrastructure.repositories.tickets_repository import TicketRepository
from src.usecases.tickets.parse.parsers.base import TicketsParser


class ParseAviaTickets:
    def __init__(
        self, parsers: list[TicketsParser], airports_repository: AirportRepository, ticket_repository: TicketRepository
    ) -> None:
        self._parsers = parsers
        self.airports_repository = airports_repository
        self.ticket_repository = ticket_repository

    async def get_exist_tickets_as_crate_dto(self) -> list[CreateAviaTicketDTO]:
        exist_tickets = await self.ticket_repository.all()
        return {
            CreateAviaTicketDTO(
                origin_airport_id=ticket.origin_airport_id,
                destination_airport_id=ticket.destination_airport_id,
                departure_at=ticket.departure_at,
                return_at=ticket.return_at,
                duration=ticket.duration,
                price=ticket.price,
                airline_id=ticket.airline_id,
                transfers=ticket.transfers,
            )
            for ticket in exist_tickets
        }

    async def __call__(
        self,
        origin_airport_ids: list[int],
        destination_airport_ids: list[int],
        departure_at: datetime,
        return_at: datetime,
    ) -> None:
        parsed_tickets = set()

        for origin_airport_id in origin_airport_ids:
            for destination_airport_id in destination_airport_ids:
                origin_airport = await self.airports_repository.get(id=origin_airport_id)
                if origin_airport is None:
                    raise AirportNotFoundException(f"no airport with id = {origin_airport_id} found")

                destination_airport = await self.airports_repository.get(id=destination_airport_id)
                if destination_airport is None:
                    raise AirportNotFoundException(f"no airport with id = {destination_airport_id} found")

                for parser in self._parsers:
                    try:
                        tickets = await parser.parse(
                            origin_airport=origin_airport,
                            destination_airport=destination_airport,
                            departure_at=departure_at,
                            return_at=return_at,
                        )

                        parsed_tickets.update(tickets)
                    except FetchAPIException as e:
                        print(f"Error while fetcing tickets {e}")

        exist_tickets_as_create_dto = await self.get_exist_tickets_as_crate_dto()

        tickets_to_create = parsed_tickets - exist_tickets_as_create_dto

        return await self.ticket_repository.create_many(tickets_to_create)
