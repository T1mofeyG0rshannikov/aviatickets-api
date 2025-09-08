from src.entities.airport.airport import Airport
from src.infrastructure.persistence.db.models.models import AirportOrm
from src.infrastructure.persistence.etl_importers.base_importer import BulkSaver


class AirportsBulkSaver(BulkSaver[Airport, AirportOrm]):
    pass
