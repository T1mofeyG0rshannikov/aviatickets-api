from src.entities.city.dto import CreateCityDTO


class CitiesCsvParser:
    def execute(self, data: list[list[str]]) -> list[CreateCityDTO]:
        return [CreateCityDTO(name=row[0], name_english=row[1]) for row in data]
