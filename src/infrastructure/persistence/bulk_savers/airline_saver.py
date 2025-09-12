from src.entities.airline.airline import Airline
from src.infrastructure.persistence.bulk_savers.base_saver import BulkSaver
from src.infrastructure.persistence.db.models.models import AirlineOrm


class AirlineBulkSaver(BulkSaver[Airline, AirlineOrm]):
    pass
