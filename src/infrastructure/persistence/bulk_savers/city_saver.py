from src.entities.location.city.city import City
from src.infrastructure.persistence.bulk_savers.base_saver import BulkSaver
from src.infrastructure.persistence.db.models.models import CityOrm


class CityBulkSaver(BulkSaver[City, CityOrm]):
    pass
