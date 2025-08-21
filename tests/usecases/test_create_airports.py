import pytest

from src.application.usecases.airports.create.adapter import (
    AirportsCsvToCreateDTOAdapter,
)
from src.application.usecases.airports.create.csv_parser import AirportsCsvParser
from src.application.usecases.airports.create.usecase import CreateAirports
from src.infrastructure.repositories.airport_repository import AirportRepository
from src.infrastructure.repositories.location_repository import LocationRepository


@pytest.fixture
async def airports_csv_parser() -> AirportsCsvParser:
    return AirportsCsvParser()


@pytest.fixture
async def airports_csv_adapter() -> AirportsCsvToCreateDTOAdapter:
    return AirportsCsvToCreateDTOAdapter()


@pytest.fixture
async def create_airports(
    airport_repository: AirportRepository,
    airports_csv_parser: AirportsCsvParser,
    airports_csv_adapter: AirportsCsvToCreateDTOAdapter,
    location_repository: LocationRepository,
) -> CreateAirports:
    return CreateAirports(airport_repository, airports_csv_parser, airports_csv_adapter, location_repository)


@pytest.mark.asyncio
async def test_create_airports(create_airports: CreateAirports):
    csv_data = [
        [
            26396,
            "UUEE",
            "large_airport",
            "Sheremetyevo International Airport",
            55.972599,
            37.4146,
            622,
            "EU",
            "RU",
            "RU-MOS",
            "Moscow",
            "yes",
            "UUEE",
            "SVO",
            "UUEE",
            "",
            "http://svo.aero/en/",
            "https://en.wikipedia.org/wiki/Sheremetyevo_International_Airport",
            "MOW, Международный аэропорт Шереметьево, svo, sheremetyevo, moscow",
        ],
        [
            27223,
            "ZSPD",
            "large_airport",
            "Shanghai Pudong International Airport",
            31.1434,
            121.805,
            13,
            "AS",
            "CN",
            "CN-31",
            "Shanghai (Pudong)",
            "yes",
            "ZSPD",
            "PVG",
            "ZSPD",
            "",
            "https://www.shanghaiairport.com/index.html",
            "https://en.wikipedia.org/wiki/Shanghai_Pudong_International_Airport",
            "",
        ],
    ]

    result = await create_airports(csv_data)
    assert result is None
