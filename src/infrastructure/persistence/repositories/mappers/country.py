from src.entities.location.country.country import Country
from src.entities.value_objects.entity_id import EntityId
from src.infrastructure.persistence.db.models.models import CountryOrm


def orm_to_country(country: CountryOrm) -> Country:
    return Country(id=EntityId(country.id), iso=country.iso, name=country.name, name_english=country.name_english)
