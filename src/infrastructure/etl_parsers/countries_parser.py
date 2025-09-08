from src.application.dto.location import CreateCountryDTO
from src.application.usecases.country.import_countries.loader import CountriesLoader


class CountriesCsvParser(CountriesLoader):
    def __init__(self, data: list[list[str]]) -> None:
        self._data = data

    def load(self) -> list[CreateCountryDTO]:
        return [CreateCountryDTO(iso=row[0], name=row[1], name_english=row[2]) for row in self._data]
