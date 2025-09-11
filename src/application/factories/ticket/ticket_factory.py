from src.application.dto.ticket import CreateTicketDTO
from src.application.factories.ticket.ticket_segment_factory import TicketSegmentFactory
from src.entities.airport.airport import Airport
from src.entities.airport.airport_repository import AirportRepositoryInterface
from src.entities.tickets.ticket_entity.ticket import Ticket
from src.entities.tickets.ticket_entity.ticket_itinerary import TicketItinerary
from src.entities.value_objects.entity_id import EntityId
from src.entities.value_objects.price.price import Price


class TicketFactory:
    def __init__(self, airport_repository: AirportRepositoryInterface) -> None:
        self.airport_repository = airport_repository

    async def create(self, ticket_dto: CreateTicketDTO) -> Ticket:
        airports: dict[EntityId, Airport] = dict()

        itineraries = []

        for itinerary in ticket_dto.itineraries:
            segments = []
            for segment in itinerary.segments:
                segments.append(
                    TicketSegmentFactory.create(
                        flight_number=segment.flight_number,
                        segment_number=segment.segment_number,
                        origin_airport=airports[EntityId(segment.origin_airport_id)],
                        destination_airport=airports[EntityId(segment.destination_airport_id)],
                        airline_id=segment.airline_id,
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
