from src.depends.annotations.db_annotation import DbAnnotation
from src.infrastructure.repositories.airlline_repository import AirlineRepository
from src.infrastructure.repositories.airport_repository import AirportRepository
from src.infrastructure.repositories.location_repository import LocationRepository
from src.infrastructure.repositories.tickets_repository import TicketRepository
from src.infrastructure.repositories.user_repository import UserRepository
from src.infrastructure.repositories.user_ticket_repository import UserTicketRepository
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


def get_user_repository(db: DbAnnotation) -> UserRepository:
    return UserRepository(db)


def get_user_ticket_repository(db: DbAnnotation) -> UserTicketRepository:
    return UserTicketRepository(db)
