from src.application.persistence.etl_importers.airline_importer import (
    AirlineImporterInterface,
)
from src.application.persistence.etl_importers.city_importer import (
    CityImporterInterface,
)
from src.application.persistence.etl_importers.country_importer import (
    CountryImporterInterface,
)
from src.application.persistence.etl_importers.region_importer import (
    RegionImporterInterface,
)
from src.infrastructure.persistence.db.models.models import AirportOrm
from src.infrastructure.persistence.etl_importers.airline_importer import (
    AirlineImporter,
)
from src.infrastructure.persistence.etl_importers.airport_importer import (
    AirportsBulkSaver,
)
from src.infrastructure.persistence.etl_importers.city_importer import CityImporter
from src.infrastructure.persistence.etl_importers.country_importer import (
    CountryImporter,
)
from src.infrastructure.persistence.etl_importers.region_importer import RegionImporter
from src.web.depends.annotations.db_annotation import DbAnnotation


def get_airport_importer(db: DbAnnotation) -> AirportsBulkSaver:
    return AirportsBulkSaver(db, AirportOrm)


def get_airline_importer(db: DbAnnotation) -> AirlineImporterInterface:
    return AirlineImporter(db)


def get_city_importer(db: DbAnnotation) -> CityImporterInterface:
    return CityImporter(db)


def get_country_importer(db: DbAnnotation) -> CountryImporterInterface:
    return CountryImporter(db)


def get_region_importer(db: DbAnnotation) -> RegionImporterInterface:
    return RegionImporter(db)
