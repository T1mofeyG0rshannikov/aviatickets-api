import pytest

from src.application.dto.bulk_result import BulkResult
from src.application.persistence.etl_importers.airport_importer import (
    AirportBulkSaverInterface,
)
from src.application.persistence.etl_importers.country_importer import (
    CountryImporterInterface,
)
from src.application.persistence.etl_importers.region_importer import (
    RegionImporterInterface,
)
from src.application.usecases.airports.import_airports.adapter import (
    AirportLoadDataToCreateDTO,
)
from src.application.usecases.airports.import_airports.loader import AirportsLoader
from src.application.usecases.airports.import_airports.usecase import ImportAirports
from src.application.usecases.country.get_or_create_countries_by_iso import (
    GetOrCreateCountriesByISO,
)
from src.application.usecases.country.persist_countries import PersistCountries
from src.application.usecases.region.get_or_create_regions_by_iso import (
    GetOrCreateRegionsByISO,
)
from src.application.usecases.region.persist_regions import PersistRegions
from src.entities.location.location_repository import LocationRepositoryInterface
from src.infrastructure.etl_parsers.airports_parser import AirportsCsvParser
from src.infrastructure.persistence.db.models.models import AirportOrm
from src.infrastructure.persistence.etl_importers.airport_importer import (
    AirportsBulkSaver,
)
from src.infrastructure.persistence.etl_importers.country_importer import (
    CountryImporter,
)
from src.infrastructure.persistence.etl_importers.region_importer import RegionImporter
from src.infrastructure.persistence.repositories.airport_repository import (
    AirportRepository,
)
from src.infrastructure.persistence.repositories.location_repository import (
    LocationRepository,
)


@pytest.fixture
async def adapter() -> AirportLoadDataToCreateDTO:
    return AirportLoadDataToCreateDTO()


@pytest.fixture
async def importer(db) -> AirportsBulkSaver:
    return AirportsBulkSaver(db, AirportOrm)


@pytest.fixture
async def loader() -> AirportsLoader:
    return AirportsCsvParser([])


@pytest.fixture
def region_importer(db) -> RegionImporterInterface:
    return RegionImporter(db)


@pytest.fixture
def country_importer(db) -> CountryImporterInterface:
    return CountryImporter(db)


@pytest.fixture
def persist_regions(
    region_importer: RegionImporterInterface,
) -> PersistRegions:
    return PersistRegions(region_importer)


@pytest.fixture
def persist_countries(
    country_importer: CountryImporterInterface,
) -> PersistCountries:
    return PersistCountries(country_importer)


@pytest.fixture
def get_or_create_regions(
    persist_regions: PersistRegions, location_repository: LocationRepositoryInterface
) -> GetOrCreateRegionsByISO:
    return GetOrCreateRegionsByISO(persist_regions, location_repository)


@pytest.fixture
def get_or_create_countries(
    persist_countries: PersistCountries, location_repository: LocationRepositoryInterface
) -> GetOrCreateCountriesByISO:
    return GetOrCreateCountriesByISO(persist_countries, location_repository)


@pytest.fixture
async def create_airports(
    airport_repository: AirportRepository,
    importer: AirportBulkSaverInterface,
    location_repository: LocationRepository,
    loader: AirportsLoader,
    adapter: AirportLoadDataToCreateDTO,
    get_or_create_regions: GetOrCreateRegionsByISO,
    get_or_create_countries: GetOrCreateCountriesByISO,
    db,
) -> ImportAirports:
    return ImportAirports(
        transaction=db,
        repository=airport_repository,
        saver=importer,
        loader=loader,
        location_repository=location_repository,
        adapter=adapter,
        get_or_create_countries_by_iso=get_or_create_countries,
        get_or_create_regions_by_iso=get_or_create_regions,
    )


@pytest.mark.asyncio
async def test_create_airports(
    create_airports: ImportAirports,
    populate_countries_db,
    populate_cities_db,
    populate_regions_db,
):
    csv_data = [
        [
            "26396",
            "UUEE",
            "large_airport",
            "Sheremetyevo International Airport",
            "55.972599",
            "37.4146",
            "622",
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
            "27223",
            "ZSPD",
            "large_airport",
            "Shanghai Pudong International Airport",
            "31.1434",
            "121.805",
            "13",
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

    loader = AirportsCsvParser(csv_data)

    create_airports.loader = loader

    expected_result = BulkResult(inserted=2, invalid=0, skipped=0)
    result = await create_airports()
    assert result == expected_result


@pytest.mark.asyncio
async def test_create_airports_with_skipped(create_airports: ImportAirports, populate_db, adapter, location_repository):
    csv_data = [
        [
            "26396",
            "UUEE",
            "large_airport",
            "Sheremetyevo International Airport",
            "55.972599",
            "37.4146",
            "622",
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
            "26396",
            "UUEE",
            "large_airport",
            "Sheremetyevo International Airport",
            "55.972599",
            "37.4146",
            "622",
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

    loader = AirportsCsvParser(csv_data)

    create_airports.loader = loader

    expected_result = BulkResult(inserted=0, invalid=0, skipped=2)
    result = await create_airports()
    assert result == expected_result


@pytest.mark.asyncio
async def test_create_airports_with_invalids(
    create_airports: ImportAirports,
    adapter,
    location_repository,
    populate_countries_db,
    populate_cities_db,
    populate_regions_db,
):
    csv_data = [
        [
            "26396",
            "UUEE1313",
            "large_airport",
            "Sheremetyevo International Airport",
            "55.972599",
            "37.4146",
            "622",
            "EU",
            "RU",
            "RU-MOS",
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
            "27223",
            "ZSPD3131",
            "large_airport",
            "Shanghai Pudong International Airport",
            "31.1434",
            "121.805",
            "13",
            "AS",
            "CN",
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

    loader = AirportsCsvParser(csv_data)

    create_airports.loader = loader

    expected_result = BulkResult(inserted=0, invalid=2, skipped=0)
    result = await create_airports()
    assert result == expected_result
