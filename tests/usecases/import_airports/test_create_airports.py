import mocks
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
    AirportLoadDataToCreateDTOAdapter,
)
from src.application.usecases.airports.import_airports.load_data_to_create_dto_adapter import (
    ConvertAirportLoadDataToCreateData,
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
async def adapter() -> AirportLoadDataToCreateDTOAdapter:
    return AirportLoadDataToCreateDTOAdapter()


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
