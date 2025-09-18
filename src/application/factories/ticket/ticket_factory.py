from entities.exceptions import AirportNotFoundError
from src.application.dto.ticket import CreateTicketDTO
from src.application.factories.ticket.ticket_segment_factory import TicketSegmentFactory
from src.entities.airport.airport_repository import AirportRepositoryInterface
from src.entities.tickets.ticket_entity.ticket import Ticket
from src.entities.tickets.ticket_entity.ticket_itinerary import TicketItinerary
from src.entities.value_objects.entity_id import EntityId
from src.entities.value_objects.price.price import Price


class TicketFactory:
    def __init__(self, airport_repository: AirportRepositoryInterface) -> None:
        self.airport_repositpory = airport_repository

    async def create(self, ticket_dto: CreateTicketDTO) -> Ticket:
        itineraries = []
        for itinerary in ticket_dto.itineraries:
            segments = []
            for segment in itinerary.segments:
                origin_airport = await self.airport_repositpory.get(id=EntityId(value=segment.origin_airport_id))

                if origin_airport is None:
                    raise AirportNotFoundError(f"airport with id = '{segment.origin_airport_id}' not found")

                destination_airport = await self.airport_repositpory.get(
                    id=EntityId(value=segment.destination_airport_id)
                )

                if destination_airport is None:
                    raise AirportNotFoundError(f"airport with id = '{segment.destination_airport_id}' not found")

                segments.append(
                    TicketSegmentFactory.create(
                        flight_number=segment.flight_number,
                        segment_number=segment.segment_number,
                        origin_airport=origin_airport,
                        destination_airport=destination_airport,
                        airline_id=segment.airline_id,
                        aircraft_id=segment.aircraft_id,
                        departure_at=segment.departure_at,
                        return_at=segment.return_at,
                        duration=segment.duration,
                        seat_class=segment.seat_class,
                        status=segment.status,
                    )
                )

            itineraries.append(
                TicketItinerary.create(
                    segments=segments,
                    duration=itinerary.duration,
                )
            )

        return Ticket.create(
            price=Price(value=ticket_dto.price, currency=ticket_dto.currency),
            itineraries=itineraries,
        )
