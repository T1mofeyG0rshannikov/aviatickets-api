from src.depends.annotations.db_annotation import DbAnnotation
from src.repositories.airlline_repository import AirlineRepository
from src.repositories.airport_repository import AirportRepository
from src.repositories.location_repository import LocationRepository
from src.repositories.tickets_repository import TicketRepository
from src.usecases.tickets.filter.repository.tickets_repository import (
    TicketReadRepository,
)


def get_airports_repository(db: DbAnnotation) -> AirportRepository:
    return AirportRepository(db)


def get_location_repository(db: DbAnnotation) -> LocationRepository:
    return LocationRepository(db)


def get_airline_repository(db: DbAnnotation) -> AirlineRepository:
    return AirlineRepository(db)


def get_ticket_repository(db: DbAnnotation) -> TicketRepository:
    return TicketRepository(db)


def get_ticket_read_repository(db: DbAnnotation) -> TicketReadRepository:
    return TicketReadRepository(db)
