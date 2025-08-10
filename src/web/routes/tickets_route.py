from typing import Annotated, List

from fastapi import APIRouter, Depends

from src.depends.depends import (
    get_create_airlines_interactor,
    get_create_airports_interactor,
    get_create_cities_interactor,
    get_create_countries_interactor,
    get_create_regions_interactor,
    get_filter_tickets_interactor,
    get_parse_tickets_interactor,
)
from src.depends.files_from_request import get_csv_file, get_txt_file
from src.entities.tickets.filters import TicketsFilter
from src.entities.user import User
from src.usecases.create_airlines.usecase import CreateAirlines
from src.usecases.create_airports.usecase import CreateAirports
from src.usecases.create_cities.usecase import CreateCities
from src.usecases.create_countries.usecase import CreateCountries
from src.usecases.create_regions.usecase import CreateRegions
from src.usecases.tickets.filter.usecase import FilterTickets
from src.usecases.tickets.parse.usecase import ParseAviaTickets
from src.web.routes.base import admin_required, get_user
from src.web.schemas.tickets import (
    FilterTicketsRequest,
    ParseTicketsRequest,
    TicketFullInfoResponse,
)

router = APIRouter(prefix="", tags=["tickets"])


@router.post("/airports/", status_code=201)
@admin_required
async def add_airports(
    user: Annotated[User, Depends(get_user)],
    usecase: Annotated[CreateAirports, Depends(get_create_airports_interactor)],
    csv_data=Depends(get_csv_file),
):
    return await usecase(csv_data)


@router.post("/airlines/", status_code=201)
@admin_required
async def add_airlines(
    user: Annotated[User, Depends(get_user)],
    usecase: Annotated[CreateAirlines, Depends(get_create_airlines_interactor)],
    txt_data=Depends(get_txt_file),
):
    return await usecase(txt_data)


@router.post("/countries/", status_code=201)
@admin_required
async def add_countries(
    user: Annotated[User, Depends(get_user)],
    usecase: Annotated[CreateCountries, Depends(get_create_countries_interactor)],
    csv_data=Depends(get_csv_file),
):
    return await usecase(csv_data)


@router.post("/regions/", status_code=201)
@admin_required
async def add_regions(
    user: Annotated[User, Depends(get_user)],
    usecase: Annotated[CreateRegions, Depends(get_create_regions_interactor)],
    csv_data=Depends(get_csv_file),
):
    return await usecase(csv_data)


@router.post("/cities/", status_code=201)
@admin_required
async def add_cities(
    user: Annotated[User, Depends(get_user)],
    usecase: Annotated[CreateCities, Depends(get_create_cities_interactor)],
    csv_data=Depends(get_csv_file),
):
    return await usecase(csv_data)


@router.post("/tickets", status_code=201)
async def parse_tickets(
    data: ParseTicketsRequest, usecase: Annotated[ParseAviaTickets, Depends(get_parse_tickets_interactor)]
):
    return await usecase(**data.model_dump())


@router.post("/filter-tickets", status_code=200, response_model=list[TicketFullInfoResponse])
async def filter_tickets(
    data: FilterTicketsRequest, usecase: Annotated[FilterTickets, Depends(get_filter_tickets_interactor)]
) -> list[TicketFullInfoResponse]:
    return await usecase(TicketsFilter(**data.model_dump()))
