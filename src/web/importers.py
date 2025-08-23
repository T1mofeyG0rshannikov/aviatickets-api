from src.infrastructure.persistence.etl_importers.airport_importer import (
    AirportImporter,
)
from src.web.depends.annotations.db_annotation import DbAnnotation


def get_airports_importer(db: DbAnnotation) -> AirportImporter:
    return AirportImporter(db)
