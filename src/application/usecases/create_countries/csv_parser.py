from src.entities.country.dto import CreateCountryDTO
from src.entities.country.iso import ISOCode


class CountriesCsvParser:
    def execute(self, data: list[list[str]]) -> CreateCountryDTO:
        return [CreateCountryDTO(iso=row[0], name=row[1], name_english=row[2]) for row in data]
