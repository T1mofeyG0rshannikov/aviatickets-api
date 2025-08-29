import pytest

from src.application.usecases.airports.create.loader import AirportsLoader
from src.application.dto.bulk_result import BulkResult
from src.infrastructure.etl_parsers.airports_parser.adapter import CsvToAirportAdapter
from src.infrastructure.etl_parsers.airports_parser.airports_parser import AirportsCsvParser
from src.application.usecases.airports.create.usecase import CreateAirports
from src.infrastructure.persistence.etl_importers.airport_importer import (
    AirportImporter,
)
from src.infrastructure.persistence.repositories.airport_repository import (
    AirportRepository,
)
from src.infrastructure.persistence.repositories.location_repository import (
    LocationRepository,
)


@pytest.fixture
async def adapter() -> CsvToAirportAdapter:
    return CsvToAirportAdapter()


@pytest.fixture
async def importer(db) -> AirportImporter:
    return AirportImporter(db)


@pytest.fixture
async def create_airports(
    airport_repository: AirportRepository,
    importer: AirportImporter,
    location_repository: LocationRepository,
    loader: AirportsLoader = None,   
) -> CreateAirports:
    return CreateAirports(airport_repository, importer, loader, location_repository)


@pytest.mark.asyncio
async def test_create_airports(
    create_airports: CreateAirports,
    adapter: CsvToAirportAdapter,
    location_repository: LocationRepository
):
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

    loader = AirportsCsvParser(
        csv_data, adapter, location_repository
    )

    create_airports.loader = loader

    expected_result = BulkResult(inserted=2, invalid=0, skipped=0)
    result = await create_airports()
    assert result == expected_result


@pytest.mark.asyncio
async def test_create_airports_with_skipped(create_airports: CreateAirports, populate_db, adapter, location_repository):
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
    ]

    loader = AirportsCsvParser(
        csv_data, adapter, location_repository
    )

    create_airports.loader = loader
    
    expected_result = BulkResult(inserted=0, invalid=0, skipped=2)
    result = await create_airports()
    assert result == expected_result


@pytest.mark.asyncio
async def test_create_airports_with_invalids(create_airports: CreateAirports, adapter, location_repository):
    csv_data = [
        [
            26396,
            "UUEE1313",
            "large_airport",
            "Sheremetyevo International Airport",
            55.972599,
            37.4146,
            622,
            "EU",
            "RU1",
            "RU13-MOS",
            "Moscow",
            "yes",
            "UUEE35353",
            "SVO3535",
            "UUEE4343",
            "",
            "http://svo.aero/en/",
            "https://en.wikipedia.org/wiki/Sheremetyevo_International_Airport",
            "MOW, Международный аэропорт Шереметьево, svo, sheremetyevo, moscow",
        ],
        [
            27223,
            "ZSPD3131",
            "large_airport",
            "Shanghai Pudong International Airport",
            31.1434,
            121.805,
            13,
            "AS3131",
            "CN5353",
            "CN-31",
            "Shanghai (Pudong)",
            "ye3s",
            "ZSPD111",
            "PVG4343",
            "ZSPD434",
            "",
            "https://www.shanghaiairport.com/index.html",
            "https://en.wikipedia.org/wiki/Shanghai_Pudong_International_Airport",
            "",
        ],
    ]

    loader = AirportsCsvParser(
        csv_data, adapter, location_repository
    )

    create_airports.loader = loader

    expected_result = BulkResult(inserted=0, invalid=2, skipped=0)
    result = await create_airports()
    print(result)
    assert result == expected_result
