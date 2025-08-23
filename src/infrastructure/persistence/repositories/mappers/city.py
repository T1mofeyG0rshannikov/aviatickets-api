from src.entities.location.city.city import City
from src.entities.value_objects.entity_id import EntityId
from src.infrastructure.persistence.db.models.models import CityOrm


def orm_to_city(city: CityOrm) -> City:
    return City(id=EntityId(city.id), name=city.name, name_english=city.name_english)
