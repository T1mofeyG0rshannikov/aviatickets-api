from decimal import Decimal

from src.application.dto.airline import AirlineDTO
from src.application.dto.ticket import TicketFullInfoDTO, TicketSegmentFullInfoDTO
from src.infrastructure.persistence.dao.builders.airport import (
    AirportFullInfoDTOBuilder,
)
from src.infrastructure.persistence.db.models.models import TicketOrm, TicketSegmentOrm


class TicketFullInfoDTOBuilder:
    @classmethod
    def from_orm_to_segment(cls, segment: TicketSegmentOrm) -> TicketSegmentFullInfoDTO:
        return TicketSegmentFullInfoDTO(
            status=segment.status,
            seat_class=segment.seat_class,
            id=segment.id,
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
            departure_at=segment.departure_at,
            return_at=segment.return_at,
            duration=segment.duration,
        )

    @classmethod
    def from_orm(cls, ticket: TicketOrm) -> TicketFullInfoDTO:
        return TicketFullInfoDTO(
            id=ticket.id,
            segments=[cls.from_orm_to_segment(segment) for segment in ticket.segments],
            duration=ticket.duration,
            price=Decimal(ticket.price),
            currency=ticket.currency,
            transfers=ticket.transfers,
        )
