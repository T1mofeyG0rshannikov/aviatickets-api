from avia.infrastructure.persistence.repositories.aircraft_repository import (
    AircraftRepository,
)
from avia.infrastructure.persistence.repositories.airline_repository import (
    AirlineRepository,
)
from avia.infrastructure.persistence.repositories.airport_repository import (
    AirportRepository,
)
from avia.infrastructure.persistence.repositories.insurance_repository import (
    InsuranceRepository,
)
from avia.infrastructure.persistence.repositories.location_repository import (
    LocationRepository,
)
from avia.infrastructure.persistence.repositories.tickets_repository import (
    TicketRepository,
)
from avia.infrastructure.persistence.repositories.user_repository import UserRepository
from avia.infrastructure.persistence.repositories.user_ticket_repository import (
    UserTicketRepository,
)
from avia.web.depends.annotations.db_annotation import DbAnnotation


def get_airports_repository(db: DbAnnotation) -> AirportRepository:
    return AirportRepository(db)


def get_location_repository(db: DbAnnotation) -> LocationRepository:
    return LocationRepository(db)


def get_airline_repository(db: DbAnnotation) -> AirlineRepository:
    return AirlineRepository(db)


def get_ticket_repository(db: DbAnnotation) -> TicketRepository:
    return TicketRepository(db)


def get_aircraft_repository(db: DbAnnotation) -> AircraftRepository:
    return AircraftRepository(db)


def get_user_repository(db: DbAnnotation) -> UserRepository:
    return UserRepository(db)


def get_user_ticket_repository(db: DbAnnotation) -> UserTicketRepository:
    return UserTicketRepository(db)


def get_insurance_repository(db: DbAnnotation) -> InsuranceRepository:
    return InsuranceRepository(db)
