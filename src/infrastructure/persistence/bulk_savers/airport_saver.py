from src.entities.airport.airport import Airport
from src.infrastructure.persistence.bulk_savers.base_saver import BulkSaver
from src.infrastructure.persistence.db.models.models import AirportOrm


class AirportsBulkSaver(BulkSaver[Airport, AirportOrm]):
    pass
