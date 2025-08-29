from src.application.dto.location import CreateCityDTO
from src.application.usecases.create_cities.loader import CitiesLoader


class CitiesCsvParser(CitiesLoader):
    def __init__(self, data: list[list[str]]) -> None:
        self._data = data

    def load(self) -> list[CreateCityDTO]:
        return [CreateCityDTO(name=row[0], name_english=row[1]) for row in self._data]
