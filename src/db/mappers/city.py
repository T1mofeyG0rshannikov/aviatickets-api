from src.db.models.models import CityOrm
from src.entities.city import City


def orm_to_city(city: CityOrm) -> City:
    return City(id=city.id, name=city.name, name_english=city.name_english)
