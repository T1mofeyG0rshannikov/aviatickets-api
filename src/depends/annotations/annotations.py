from typing import Annotated

from fastapi import Depends

from src.depends.repositories import (
    get_airline_repository,
    get_airports_repository,
    get_location_repository,
    get_ticket_read_repository,
    get_ticket_repository,
)
from src.repositories.airlline_repository import AirlineRepository
from src.repositories.airport_repository import AirportRepository
from src.repositories.location_repository import LocationRepository
from src.repositories.tickets_repository import TicketRepository
from src.usecases.tickets.filter.repository.tickets_repository import (
    TicketReadRepository,
)

LocationRepositoryAnnotation = Annotated[LocationRepository, Depends(get_location_repository)]
AirportRepositoryAnnotation = Annotated[AirportRepository, Depends(get_airports_repository)]
AirlineRepositoryAnnotation = Annotated[AirlineRepository, Depends(get_airline_repository)]
TicketRepositoryAnnotation = Annotated[TicketRepository, Depends(get_ticket_repository)]
TicketReadRepositoryAnnotation = Annotated[TicketReadRepository, Depends(get_ticket_read_repository)]
