from src.entities.location.country.country import Country
from src.infrastructure.persistence.bulk_savers.base_saver import BulkSaver
from src.infrastructure.persistence.db.models.models import CountryOrm


class CountryBulkSaver(BulkSaver[Country, CountryOrm]):
    pass
