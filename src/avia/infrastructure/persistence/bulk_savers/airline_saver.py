from avia.entities.airline.airline import Airline
from avia.infrastructure.persistence.bulk_savers.base_saver import BulkSaver
from avia.infrastructure.persistence.db.models.models import AirlineOrm


class AirlineBulkSaver(BulkSaver[Airline, AirlineOrm]):
    pass
