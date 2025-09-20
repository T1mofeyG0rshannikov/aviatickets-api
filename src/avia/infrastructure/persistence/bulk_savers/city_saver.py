from avia.entities.location.city.city import City
from avia.infrastructure.persistence.bulk_savers.base_saver import BulkSaver
from avia.infrastructure.persistence.db.models.models import CityOrm


class CityBulkSaver(BulkSaver[City, CityOrm]):
    pass
