from src.entities.city import City
from src.infrastructure.db.models.models import CityOrm


def orm_to_city(city: CityOrm) -> City:
    return City(id=city.id, name=city.name, name_english=city.name_english)
