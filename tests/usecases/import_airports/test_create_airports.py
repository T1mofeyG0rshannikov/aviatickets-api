import mocks
import pytest
from redis import Redis  # type: ignore

from avia.application.dto.bulk_result import BulkResult
from avia.application.persistence.bulk_savers.airport_saver import (
    AirportBulkSaverInterface,
)
from avia.application.persistence.bulk_savers.country_saver import (
    CountryBulkSaverInterface,
)
from avia.application.persistence.bulk_savers.region_saver import (
    RegionBulkSaverInterface,
)
from avia.application.usecases.airports.import_airports.adapter import (
    AirportLoadDataToCreateDTOAdapter,
)
from avia.application.usecases.airports.import_airports.load_data_to_create_dto_adapter import (
    ConvertAirportLoadDataToCreateData,
)
from avia.application.usecases.airports.import_airports.loader import AirportsLoader
from avia.application.usecases.airports.import_airports.usecase import ImportAirports
from avia.application.usecases.country.get_or_create_countries_by_iso import (
    GetOrCreateCountriesByISO,
)
from avia.application.usecases.region.get_or_create_regions_by_iso import (
    GetOrCreateRegionsByISO,
)
from avia.entities.location.location_repository import LocationRepositoryInterface
from avia.infrastructure.etl_parsers.airports_parser import AirportsCsvParser
from avia.infrastructure.persistence.bulk_savers.airport_saver import AirportsBulkSaver
from avia.infrastructure.persistence.bulk_savers.country_saver import CountryBulkSaver
from avia.infrastructure.persistence.bulk_savers.region_saver import RegionBulkSaver
from avia.infrastructure.persistence.repositories.airport_repository import (
    AirportRepository,
)
from avia.infrastructure.persistence.repositories.location_repository import (
    LocationRepository,
)


@pytest.fixture
async def adapter() -> AirportLoadDataToCreateDTOAdapter:
    return AirportLoadDataToCreateDTOAdapter()


@pytest.fixture
async def importer(db) -> AirportsBulkSaver:
    return AirportsBulkSaver(db)


@pytest.fixture
async def loader() -> AirportsLoader:
    return AirportsCsvParser([])


@pytest.fixture
def regions_bulk_saver(db) -> RegionBulkSaver:
    return RegionBulkSaver(db)


@pytest.fixture
def countries_bulk_saver(db) -> CountryBulkSaver:
    return CountryBulkSaver(db)


@pytest.fixture
def get_or_create_regions(
    regions_bulk_saver: RegionBulkSaverInterface, location_repository: LocationRepositoryInterface, redis: Redis
) -> GetOrCreateRegionsByISO:
    return GetOrCreateRegionsByISO(
        regions_bulk_saver=regions_bulk_saver, location_repository=location_repository, redis=redis
    )


@pytest.fixture
def get_or_create_countries(
    countries_bulk_saver: CountryBulkSaverInterface, location_repository: LocationRepositoryInterface, redis: Redis
) -> GetOrCreateCountriesByISO:
    return GetOrCreateCountriesByISO(saver=countries_bulk_saver, location_repository=location_repository, redis=redis)


@pytest.fixture
def converter(
    location_repository: LocationRepository,
    get_or_create_regions: GetOrCreateRegionsByISO,
    get_or_create_countries: GetOrCreateCountriesByISO,
    adapter: AirportLoadDataToCreateDTOAdapter,
) -> ConvertAirportLoadDataToCreateData:
    return ConvertAirportLoadDataToCreateData(
        location_repository=location_repository,
        get_or_create_countries_by_iso=get_or_create_countries,
        get_or_create_regions_by_iso=get_or_create_regions,
        adapter=adapter,
    )


@pytest.fixture
async def create_airports(
    airport_repository: AirportRepository,
    importer: AirportBulkSaverInterface,
    loader: AirportsLoader,
    converter: ConvertAirportLoadDataToCreateData,
    db,
) -> ImportAirports:
    return ImportAirports(
        transaction=db, repository=airport_repository, saver=importer, loader=loader, converter=converter
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "csv_data, expected_result",
    [
        (mocks.VALID_AIRPORTS_DATA, BulkResult(inserted=2, invalid=0, skipped=0)),
        (mocks.INVALID_AIRPORTS_DATA, BulkResult(inserted=0, invalid=2, skipped=0)),
    ],
)
async def test_create_airports(
    create_airports: ImportAirports,
    populate_countries_db,
    populate_cities_db,
    populate_regions_db,
    csv_data,
    expected_result,
):
    loader = AirportsCsvParser(csv_data)

    create_airports.loader = loader

    result = await create_airports()
    assert result == expected_result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "csv_data, expected_result", [(mocks.AIRPORTS_DATA_WITH_SKIPPED, BulkResult(inserted=0, invalid=0, skipped=2))]
)
async def test_create_airports_with_skipped(create_airports: ImportAirports, populate_db, csv_data, expected_result):
    loader = AirportsCsvParser(csv_data)

    create_airports.loader = loader

    result = await create_airports()
    assert result == expected_result
