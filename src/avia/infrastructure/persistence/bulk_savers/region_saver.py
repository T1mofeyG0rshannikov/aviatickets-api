from avia.entities.location.region.region import Region
from avia.infrastructure.persistence.bulk_savers.base_saver import BulkSaver
from avia.infrastructure.persistence.db.models.models import RegionOrm


class RegionBulkSaver(BulkSaver[Region, RegionOrm]):
    pass
