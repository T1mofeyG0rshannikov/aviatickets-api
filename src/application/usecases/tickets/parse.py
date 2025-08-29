from datetime import datetime

from src.application.factories.ticket_segment_factory import TicketSegmentFactory
from src.entities.tickets.ticket import Ticket
from src.entities.airport.airport_repository import AirportRepositoryInterface
from src.entities.exceptions import AirportNotFoundError
from src.entities.tickets.tickets_repository import TicketRepositoryInterface
from src.interface_adapters.tickets_parser import TicketsParseParams, TicketsParser


class ParseAviaTickets:
    def __init__(
        self,
        parsers: list[TicketsParser],
        airports_repository: AirportRepositoryInterface,
        ticket_repository: TicketRepositoryInterface,
    ) -> None:
        self._parsers = parsers
        self.airports_repository = airports_repository
        self.ticket_repository = ticket_repository

    async def get_exist_tickets_hashes(self) -> set[str]:
        exist_tickets = await self.ticket_repository.all()
        return {hash(tuple(segment.flight_number for segment in ticket.segments)) for ticket in exist_tickets}

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
        parsed_tickets = []
        exist_tickets_hashes = await self.get_exist_tickets_hashes()

        for origin_airport_id in origin_airport_ids:
            for destination_airport_id in destination_airport_ids:
                origin_airport = await self.airports_repository.get(id=origin_airport_id)
                if origin_airport is None:
                    raise AirportNotFoundError(f"no airport with id = {origin_airport_id} found")

                destination_airport = await self.airports_repository.get(id=destination_airport_id)
                if destination_airport is None:
                    raise AirportNotFoundError(f"no airport with id = {destination_airport_id} found")

                for parser in self._parsers:
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

                    for ticket_dto in tickets_dto:
                        if (
                            hash(tuple(segment.flight_number for segment in ticket_dto.segments))
                            not in exist_tickets_hashes
                        ):
                            segments = [
                                TicketSegmentFactory.create(
                                    flight_number=segment_dto.flight_number,
                                    segment_number=segment_dto.segment_number,
                                    origin_airport_id=segment_dto.origin_airport_id,
                                    destination_airport_id=segment_dto.destination_airport_id,
                                    airline_id=segment_dto.airline_id,
                                    departure_at=segment_dto.departure_at,
                                    return_at=segment_dto.return_at,
                                    duration=segment_dto.duration,
                                    seat_class=segment_dto.seat_class,
                                    status=segment_dto.status
                                ) for segment_dto in ticket_dto.segments
                            ]

                            ticket = Ticket.create(
                                duration=ticket_dto.duration,
                                price=ticket_dto.price,
                                currency=ticket_dto.currency,
                                transfers=ticket_dto.transfers,
                                segments=segments
                            )

                            parsed_tickets.append(ticket)

        return await self.ticket_repository.save_many(parsed_tickets)
