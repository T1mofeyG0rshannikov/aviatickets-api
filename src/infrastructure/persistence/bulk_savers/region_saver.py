from src.entities.location.region.region import Region
from src.infrastructure.persistence.bulk_savers.base_saver import BulkSaver
from src.infrastructure.persistence.db.models.models import RegionOrm


class RegionBulkSaver(BulkSaver[Region, RegionOrm]):
    pass
