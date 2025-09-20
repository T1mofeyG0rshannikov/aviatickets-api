from datetime import datetime
from uuid import UUID

from avia.application.exceptions import FetchAPIError
from avia.application.factories.ticket.ticket_factory import TicketFactory
from avia.application.persistence.transaction import Transaction
from avia.application.tickets_parser import TicketsParseParams, TicketsParser
from avia.entities.airport.airport_repository import AirportRepositoryInterface
from avia.entities.exceptions import AirportNotFoundError
from avia.entities.tickets.ticket_entity.ticket import Ticket
from avia.entities.tickets.tickets_repository import TicketRepositoryInterface
from avia.entities.value_objects.entity_id import EntityId


class ParseAviaTickets:
    def __init__(
        self,
        parsers: list[TicketsParser],
        ticket_factory: TicketFactory,
        airports_repository: AirportRepositoryInterface,
        ticket_repository: TicketRepositoryInterface,
        transaction: Transaction,
    ) -> None:
        self.ticket_factory = ticket_factory
        self._parsers = parsers
        self.airports_repository = airports_repository
        self.ticket_repository = ticket_repository
        self.transaction = transaction

    async def __call__(
        self,
        origin_airport_ids: list[UUID],
        destination_airport_ids: list[UUID],
        departure_at: datetime,
        return_at: datetime,
        adults: int,
        childrens: int,
        infants: int,
    ) -> None:
        parsed_tickets: list[Ticket] = []
        exist_tickets_unique_keys = await self.ticket_repository.all_unique_keys()

        for origin_airport_id in origin_airport_ids:
            for destination_airport_id in destination_airport_ids:
                origin_airport = await self.airports_repository.get(id=EntityId(value=origin_airport_id))
                if origin_airport is None:
                    raise AirportNotFoundError(f"no airport with id = {origin_airport_id} found")

                destination_airport = await self.airports_repository.get(id=EntityId(value=destination_airport_id))
                if destination_airport is None:
                    raise AirportNotFoundError(f"no airport with id = {destination_airport_id} found")

                for parser in self._parsers:
                    try:
                        tickets_dto = await parser.parse(
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
                    except FetchAPIError:
                        print("error while fetching api")
                        continue

                    for ticket_dto in tickets_dto:
                        ticket = await self.ticket_factory.create(ticket_dto)

                        if ticket.unique_key not in exist_tickets_unique_keys:
                            parsed_tickets.append(ticket)

        await self.ticket_repository.save_many(parsed_tickets)
        await self.transaction.commit()
