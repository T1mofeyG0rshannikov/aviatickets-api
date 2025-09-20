from avia.entities.location.country.country import Country
from avia.infrastructure.persistence.bulk_savers.base_saver import BulkSaver
from avia.infrastructure.persistence.db.models.models import CountryOrm


class CountryBulkSaver(BulkSaver[Country, CountryOrm]):
    pass
