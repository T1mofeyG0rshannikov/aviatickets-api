from typing import Annotated

from fastapi import APIRouter, Depends

from avia.application.usecases.airports.get.usecase import GetAirports
from avia.application.usecases.city.get import GetCities
from avia.application.usecases.country.get import GetCountries
from avia.web.depends.usecases import (
    get_airports_interactor,
    get_cities_interactor,
    get_countries_interactor,
)

router = APIRouter(prefix="", tags=["filter"])


@router.get("/cities/{start_with}", status_code=200)
async def get_cities(start_with: str, usecase: Annotated[GetCities, Depends(get_cities_interactor)]):
    return await usecase(start_with)


@router.get("/countries/{start_with}", status_code=200)
async def get_countries(start_with: str, usecase: Annotated[GetCountries, Depends(get_countries_interactor)]):
    return await usecase(start_with)


@router.get("/airports/{start_with}", status_code=200)
async def get_airports(start_with: str, usecase: Annotated[GetAirports, Depends(get_airports_interactor)]):
    return await usecase(start_with)
