from typing import Annotated

from fastapi import Depends

from src.infrastructure.repositories.airlline_repository import AirlineRepository
from src.infrastructure.repositories.airport_read_repository import (
    AirportReadRepository,
)
from src.infrastructure.repositories.airport_repository import AirportRepository
from src.infrastructure.repositories.location_repository import LocationRepository
from src.infrastructure.repositories.tickets_read_repository import TicketReadRepository
from src.infrastructure.repositories.tickets_repository import TicketRepository
from src.infrastructure.repositories.user_repository import UserRepository
from src.infrastructure.repositories.user_ticket_repository import UserTicketRepository
from src.web.depends.repositories import (
    get_airline_repository,
    get_airport_read_repository,
    get_airports_repository,
    get_location_repository,
    get_ticket_read_repository,
    get_ticket_repository,
    get_user_repository,
    get_user_ticket_repository,
)

LocationRepositoryAnnotation = Annotated[LocationRepository, Depends(get_location_repository)]
AirportRepositoryAnnotation = Annotated[AirportRepository, Depends(get_airports_repository)]
AirlineRepositoryAnnotation = Annotated[AirlineRepository, Depends(get_airline_repository)]
TicketRepositoryAnnotation = Annotated[TicketRepository, Depends(get_ticket_repository)]
TicketReadRepositoryAnnotation = Annotated[TicketReadRepository, Depends(get_ticket_read_repository)]
AirportReadRepositoryAnnotation = Annotated[AirportReadRepository, Depends(get_airport_read_repository)]
UserRepositoryAnnotation = Annotated[UserRepository, Depends(get_user_repository)]
UserTicketRepositoryAnnotation = Annotated[UserTicketRepository, Depends(get_user_ticket_repository)]
