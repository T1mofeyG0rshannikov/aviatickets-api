from typing import Annotated

from fastapi import APIRouter, Depends

from src.application.usecases.airports.create.usecase import CreateAirports
from src.application.usecases.airports.get.usecase import GetAirports
from src.application.usecases.create_airlines.usecase import CreateAirlines
from src.application.usecases.create_cities.usecase import CreateCities
from src.application.usecases.create_countries.usecase import CreateCountries
from src.application.usecases.create_regions.usecase import CreateRegions
from src.application.usecases.tickets.filter import FilterTickets
from src.application.usecases.tickets.get import GetTicket
from src.application.usecases.tickets.parse import ParseAviaTickets
from src.entities.tickets.filters import TicketsFilter
from src.web.depends.annotations.user_annotation import UserAnnotation
from src.web.depends.files_from_request import get_csv_file, get_txt_file
from src.web.depends.usecases import (
    get_airports_interactor,
    get_create_airlines_interactor,
    get_create_airports_interactor,
    get_create_cities_interactor,
    get_create_countries_interactor,
    get_create_regions_interactor,
    get_filter_tickets_interactor,
    get_parse_tickets_interactor,
    get_ticket_interactor,
)
from src.web.routes.base import admin_required
from src.web.schemas.tickets import FilterTicketsRequest, ParseTicketsRequest

router = APIRouter(prefix="", tags=["tickets"])


@router.post("/airports/", status_code=201)
@admin_required
async def add_airports(
    user: UserAnnotation,
    usecase: Annotated[CreateAirports, Depends(get_create_airports_interactor)],
    csv_data=Depends(get_csv_file),
):
    return await usecase(csv_data)


@router.post("/airlines/", status_code=201)
@admin_required
async def add_airlines(
    user: UserAnnotation,
    usecase: Annotated[CreateAirlines, Depends(get_create_airlines_interactor)],
    txt_data=Depends(get_txt_file),
):
    return await usecase(txt_data)


@router.post("/countries/", status_code=201)
@admin_required
async def add_countries(
    user: UserAnnotation,
    usecase: Annotated[CreateCountries, Depends(get_create_countries_interactor)],
    csv_data=Depends(get_csv_file),
):
    return await usecase(csv_data)


@router.post("/regions/", status_code=201)
@admin_required
async def add_regions(
    user: UserAnnotation,
    usecase: Annotated[CreateRegions, Depends(get_create_regions_interactor)],
    csv_data=Depends(get_csv_file),
):
    return await usecase(csv_data)


@router.post("/cities/", status_code=201)
@admin_required
async def add_cities(
    user: UserAnnotation,
    usecase: Annotated[CreateCities, Depends(get_create_cities_interactor)],
    csv_data=Depends(get_csv_file),
):
    return await usecase(csv_data)


@router.post("/tickets", status_code=201)
async def parse_tickets(
    data: ParseTicketsRequest, usecase: Annotated[ParseAviaTickets, Depends(get_parse_tickets_interactor)]
):
    return await usecase(**data.model_dump())


@router.post("/filter-tickets", status_code=200)
async def filter_tickets(
    data: FilterTicketsRequest, usecase: Annotated[FilterTickets, Depends(get_filter_tickets_interactor)]
):
    return await usecase(TicketsFilter(**data.model_dump()))


@router.get("/ticket/{ticket_id}", status_code=200)
async def get_ticket(ticket_id: int, usecase: Annotated[GetTicket, Depends(get_ticket_interactor)]):
    return await usecase(ticket_id)


@router.get("/airports/{start_with}", status_code=200)
async def get_airports(start_with: str, usecase: Annotated[GetAirports, Depends(get_airports_interactor)]):
    return await usecase(start_with)
