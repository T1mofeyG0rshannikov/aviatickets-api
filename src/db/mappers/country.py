from src.db.models.models import CountryOrm
from src.entities.country.country import Country


def orm_to_country(country: CountryOrm) -> Country:
    return Country(id=country.id, iso=country.iso, name=country.name, name_english=country.name_english)
