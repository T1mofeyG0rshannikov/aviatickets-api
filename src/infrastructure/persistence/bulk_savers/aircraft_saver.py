from src.entities.aircraft.entity import Aircraft
from src.infrastructure.persistence.bulk_savers.base_saver import BulkSaver
from src.infrastructure.persistence.db.models.models import AircraftOrm


class AircraftBulkSaver(BulkSaver[Aircraft, AircraftOrm]):
    pass
