from avia.entities.aircraft.entity import Aircraft
from avia.infrastructure.persistence.bulk_savers.base_saver import BulkSaver
from avia.infrastructure.persistence.db.models.models import AircraftOrm


class AircraftBulkSaver(BulkSaver[Aircraft, AircraftOrm]):
    pass
