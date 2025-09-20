from decimal import Decimal

from avia.application.dto.aircraft import AircraftDTO
from avia.application.dto.airline import AirlineDTO
from avia.application.dto.ticket import (
    TicketFullInfoDTO,
    TicketItineraryFullInfoDTO,
    TicketSegmentFullInfoDTO,
)
from avia.infrastructure.persistence.dao.builders.airport import (
    AirportFullInfoDTOBuilder,
)
from avia.infrastructure.persistence.db.models.models import (
    TicketItineraryOrm,
    TicketOrm,
    TicketSegmentOrm,
)


class TicketFullInfoDTOBuilder:
    @classmethod
    def from_orm_to_segment(cls, segment: TicketSegmentOrm) -> TicketSegmentFullInfoDTO:
        return TicketSegmentFullInfoDTO(
            status=segment.status,
            seat_class=segment.seat_class,
            segment_number=segment.segment_number,
            flight_number=segment.flight_number,
            destination_airport=AirportFullInfoDTOBuilder.from_orm(segment.destination_airport),
            origin_airport=AirportFullInfoDTOBuilder.from_orm(segment.origin_airport),
            airline=AirlineDTO(
                id=segment.airline.id,
                iata=segment.airline.iata,
                icao=segment.airline.icao,
                name=segment.airline.name,
                name_russian=segment.airline.name_russian,
            ),
            aircraft=AircraftDTO(name=segment.aircraft.name, iata=segment.aircraft.iata),
            departure_at=segment.departure_at,
            return_at=segment.return_at,
            duration=segment.duration,
        )

    @classmethod
    def from_orm_to_itinerary(cls, itinerary: TicketItineraryOrm) -> TicketItineraryFullInfoDTO:
        return TicketItineraryFullInfoDTO(
            transfers=itinerary.transfers,
            segments=[cls.from_orm_to_segment(segment) for segment in itinerary.segments],
            duration=itinerary.duration,
        )

    @classmethod
    def from_orm(cls, ticket: TicketOrm) -> TicketFullInfoDTO:
        return TicketFullInfoDTO(
            id=ticket.id,
            itineraries=[cls.from_orm_to_itinerary(segment) for segment in ticket.itineraries],
            price=Decimal(ticket.price),
            currency=ticket.currency,
        )
