from src.application.dto.ticket import CreateTicketDTO
from src.application.factories.ticket.ticket_segment_factory import TicketSegmentFactory
from src.entities.tickets.ticket_entity.ticket import Ticket
from src.entities.tickets.ticket_entity.ticket_itinerary import TicketItinerary
from src.entities.value_objects.price.price import Price


class TicketFactory:
    @classmethod
    def create(cls, ticket_dto: CreateTicketDTO) -> Ticket:
        return Ticket.create(
            price=Price(value=ticket_dto.price, currency=ticket_dto.currency),
            itineraries=[
                TicketItinerary.create(
                    segments=[
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
                            status=segment_dto.status,
                        )
                        for segment_dto in itinerary.segments
                    ],
                    duration=itinerary.duration,
                )
                for itinerary in ticket_dto.itineraries
            ],
        )
