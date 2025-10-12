from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from avia.application.dto.ticket import ListTicketDTO, TicketFullInfoDTO
from avia.application.usecases.aircraft.import_aircrafts.usecase import ImportAircrafts
from avia.application.usecases.airline.import_airlines.usecase import ImportAirlines
from avia.application.usecases.airports.get.usecase import GetAirports
from avia.application.usecases.airports.import_airports.usecase import ImportAirports
from avia.application.usecases.city.import_cities.usecase import CreateCities
from avia.application.usecases.country.import_countries.usecase import ImportCountries
from avia.application.usecases.region.import_regions.usecase import ImportRegions
from avia.application.usecases.tickets.filter import FilterTickets
from avia.application.usecases.tickets.get import GetTicket
from avia.application.usecases.tickets.parse import ParseAviaTickets
from avia.entities.tickets.filters import TicketsFilter
from avia.entities.value_objects.entity_id import EntityId
from avia.web.depends.annotations.user_annotation import UserAnnotation
from avia.web.depends.usecases import (
    get_airports_interactor,
    get_create_airlines_interactor,
    get_create_airports_interactor,
    get_create_cities_interactor,
    get_create_countries_interactor,
    get_create_regions_interactor,
    get_filter_tickets_interactor,
    get_import_aircrafts_interactor,
    get_parse_tickets_interactor,
    get_ticket_interactor,
)
from avia.web.routes.base import admin_required
from avia.web.schemas.tickets import FilterTicketsRequest, ParseTicketsRequest

router = APIRouter(prefix="", tags=["tickets"])


@router.post("/airports/", status_code=201)
@admin_required
async def add_airports(
    user: UserAnnotation,
    usecase: Annotated[ImportAirports, Depends(get_create_airports_interactor)],
):
    return await usecase()


@router.post("/airlines/", status_code=201)
@admin_required
async def add_airlines(
    user: UserAnnotation, usecase: Annotated[ImportAirlines, Depends(get_create_airlines_interactor)]
):
    return await usecase()


@router.post("/countries/", status_code=201)
@admin_required
async def add_countries(
    user: UserAnnotation,
    usecase: Annotated[ImportCountries, Depends(get_create_countries_interactor)],
):
    return await usecase()


@router.post("/regions/", status_code=201)
@admin_required
async def add_regions(
    user: UserAnnotation,
    usecase: Annotated[ImportRegions, Depends(get_create_regions_interactor)],
):
    return await usecase()


@router.post("/aircrafts/", status_code=201)
@admin_required
async def add_aircrafts(
    user: UserAnnotation,
    usecase: Annotated[ImportAircrafts, Depends(get_import_aircrafts_interactor)],
):
    return await usecase()


@router.post("/cities/", status_code=201)
@admin_required
async def add_cities(
    user: UserAnnotation,
    usecase: Annotated[CreateCities, Depends(get_create_cities_interactor)],
):
    return await usecase()


@router.post("/tickets", status_code=201)
async def parse_tickets(
    data: ParseTicketsRequest, usecase: Annotated[ParseAviaTickets, Depends(get_parse_tickets_interactor)]
):
    return await usecase(**data.model_dump())


@router.post("/filter-tickets", status_code=200, response_model=list[ListTicketDTO])
async def filter_tickets(
    data: FilterTicketsRequest, usecase: Annotated[FilterTickets, Depends(get_filter_tickets_interactor)]
) -> list[ListTicketDTO]:
    return await usecase(TicketsFilter(**data.model_dump()))


@router.get("/ticket/{ticket_id}", status_code=200)
async def get_ticket(ticket_id: UUID, usecase: Annotated[GetTicket, Depends(get_ticket_interactor)]):
    return await usecase(EntityId(value=ticket_id))


@router.get("/airports/{start_with}", status_code=200)
async def get_airports(start_with: str, usecase: Annotated[GetAirports, Depends(get_airports_interactor)]):
    return await usecase(start_with)
