from src.dto.airport import AirportFullInfoDTO
from src.infrastructure.db.mappers.airline import from_orm_to_airline
from src.infrastructure.db.mappers.city import orm_to_city
from src.infrastructure.db.mappers.country import orm_to_country
from src.infrastructure.db.mappers.region import orm_to_region
from src.infrastructure.db.models.models import AirportOrm, TicketOrm
from src.usecases.tickets.filter.dto import TicketFullInfoDTO


class AirportFullInfoDTOBuilder:
    @classmethod
    def from_orm(cls, airport: AirportOrm) -> AirportFullInfoDTO:
        return AirportFullInfoDTO(
            id=airport.id,
            name=airport.name,
            continent=airport.continent,
            country=orm_to_country(airport.country) if airport.country else None,
            region=orm_to_region(airport.region) if airport.region else None,
            city=orm_to_city(airport.city) if airport.city else None,
            scheduled_service=airport.scheduled_service,
            icao=airport.icao,
            iata=airport.iata,
            gps_code=airport.gps_code,
            name_russian=airport.name_russian,
        )


class TicketFullInfoDTOBuilder:
    @classmethod
    def from_orm(cls, ticket: TicketOrm) -> TicketFullInfoDTO:
        return TicketFullInfoDTO(
            id=ticket.id,
            origin_airport=AirportFullInfoDTOBuilder.from_orm(ticket.origin_airport),
            destination_airport=AirportFullInfoDTOBuilder.from_orm(ticket.destination_airport),
            airline=from_orm_to_airline(ticket.airline),
            departure_at=ticket.departure_at,
            return_at=ticket.return_at,
            duration=ticket.duration,
            price=ticket.price,
            transfers=ticket.transfers,
        )
