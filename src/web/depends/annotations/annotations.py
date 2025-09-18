from typing import Annotated

from fastapi import Depends

from src.infrastructure.persistence.dao.airport_dao import AirportDAO
from src.infrastructure.persistence.dao.cities_dao import CitiestDAO
from src.infrastructure.persistence.dao.countries_dao import CountriesDAO
from src.infrastructure.persistence.dao.tickets_dao import TicketDAO
from src.infrastructure.persistence.repositories.aircraft_repository import (
    AircraftRepository,
)
from src.infrastructure.persistence.repositories.airline_repository import (
    AirlineRepository,
)
from src.infrastructure.persistence.repositories.airport_repository import (
    AirportRepository,
)
from src.infrastructure.persistence.repositories.insurance_repository import (
    InsuranceRepository,
)
from src.infrastructure.persistence.repositories.location_repository import (
    LocationRepository,
)
from src.infrastructure.persistence.repositories.tickets_repository import (
    TicketRepository,
)
from src.infrastructure.persistence.repositories.user_repository import UserRepository
from src.infrastructure.persistence.repositories.user_ticket_repository import (
    UserTicketRepository,
)
from src.web.depends.dao import (
    get_airport_dao,
    get_cities_dao,
    get_countries_dao,
    get_ticket_dao,
)
from src.web.depends.repositories import (
    get_aircraft_repository,
    get_airline_repository,
    get_airports_repository,
    get_insurance_repository,
    get_location_repository,
    get_ticket_repository,
    get_user_repository,
    get_user_ticket_repository,
)

LocationRepositoryAnnotation = Annotated[LocationRepository, Depends(get_location_repository)]
AirportRepositoryAnnotation = Annotated[AirportRepository, Depends(get_airports_repository)]
AirlineRepositoryAnnotation = Annotated[AirlineRepository, Depends(get_airline_repository)]
TicketRepositoryAnnotation = Annotated[TicketRepository, Depends(get_ticket_repository)]
AircraftRepositoryAnnotation = Annotated[AircraftRepository, Depends(get_aircraft_repository)]
TicketDAOAnnotation = Annotated[TicketDAO, Depends(get_ticket_dao)]
AirportDAOAnnotation = Annotated[AirportDAO, Depends(get_airport_dao)]
CitiesDAOAnnotation = Annotated[CitiestDAO, Depends(get_cities_dao)]
CountriesDAOAnnotation = Annotated[CountriesDAO, Depends(get_countries_dao)]
UserRepositoryAnnotation = Annotated[UserRepository, Depends(get_user_repository)]
UserTicketRepositoryAnnotation = Annotated[UserTicketRepository, Depends(get_user_ticket_repository)]
InsuranceRepositoryAnnotation = Annotated[InsuranceRepository, Depends(get_insurance_repository)]
