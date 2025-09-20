from avia.entities.airport.airport import Airport
from avia.infrastructure.persistence.bulk_savers.base_saver import BulkSaver
from avia.infrastructure.persistence.db.models.models import AirportOrm


class AirportsBulkSaver(BulkSaver[Airport, AirportOrm]):
    pass
