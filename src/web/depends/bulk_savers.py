from src.infrastructure.persistence.bulk_savers.airline_saver import AirlineBulkSaver
from src.infrastructure.persistence.bulk_savers.airport_saver import AirportsBulkSaver
from src.infrastructure.persistence.bulk_savers.city_saver import CityBulkSaver
from src.infrastructure.persistence.bulk_savers.country_saver import CountryBulkSaver
from src.infrastructure.persistence.bulk_savers.region_saver import RegionBulkSaver
from src.web.depends.annotations.db_annotation import DbAnnotation


def get_airport_importer(db: DbAnnotation) -> AirportsBulkSaver:
    return AirportsBulkSaver(db)


def get_airline_importer(db: DbAnnotation) -> AirlineBulkSaver:
    return AirlineBulkSaver(db)


def get_city_importer(db: DbAnnotation) -> CityBulkSaver:
    return CityBulkSaver(db)


def get_country_importer(db: DbAnnotation) -> CountryBulkSaver:
    return CountryBulkSaver(db)


def get_region_importer(db: DbAnnotation) -> RegionBulkSaver:
    return RegionBulkSaver(db)
