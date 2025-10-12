
from decimal import Decimal
from avia.application.dto.airline import AirlineDTO
from avia.application.dto.ticket import ListTicketDTO, ListTicketItineraryDTO, TicketSegmentFullInfoDTO
from avia.infrastructure.persistence.dao.builders.airport import AirportFullInfoDTOBuilder
from avia.infrastructure.persistence.dao.builders.ticket import TicketFullInfoDTOBuilder
from avia.infrastructure.persistence.db.models.models import TicketItineraryOrm, TicketOrm


class ListTicketDTOBuilder:
    @classmethod
    def from_orm_to_segments(cls, itinerary: TicketItineraryOrm) -> TicketSegmentFullInfoDTO:
        return sorted([TicketFullInfoDTOBuilder.from_orm_to_segment(segment) for segment in itinerary.segments], key=lambda s: s.segment_number)

    @classmethod
    def from_orm_to_list_itinerary(cls, itinerary: TicketItineraryOrm) -> ListTicketItineraryDTO:
        segments = ListTicketDTOBuilder.from_orm_to_segments(itinerary)

        return ListTicketItineraryDTO(
            transfers=itinerary.transfers,
            duration=itinerary.duration,
            origin_airport=AirportFullInfoDTOBuilder.from_orm(segments[0].origin_airport),
            destination_airport=AirportFullInfoDTOBuilder.from_orm(segments[-1].destination_airport),
            departure_at=segments[0].departure_at,
            return_at=segments[-1].return_at,
            airline=AirlineDTO(
                id=segments[0].airline.id,
                iata=segments[0].airline.iata,
                icao=segments[0].airline.icao,
                name=segments[0].airline.name,
                name_russian=segments[0].airline.name_russian,
            )
        )

    @classmethod
    def from_orm(cls, ticket: TicketOrm) -> ListTicketDTO:
        itineraries = [cls.from_orm_to_list_itinerary(itinerary) for itinerary in ticket.itineraries]

        itineraries = sorted(itineraries, key=lambda i: i.departure_at)
    
        return ListTicketDTO(
            id=ticket.id,
            price=Decimal(ticket.price),
            currency=ticket.currency,
            itineraries=itineraries,
        )
