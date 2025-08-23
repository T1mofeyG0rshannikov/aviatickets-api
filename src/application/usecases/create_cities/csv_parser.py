from src.entities.location.city.city import City
from src.entities.value_objects.entity_id import EntityId


class CitiesCsvParser:
    def execute(self, data: list[list[str]]) -> list[City]:
        return [City.create(name=row[0], name_english=row[1]) for row in data]
