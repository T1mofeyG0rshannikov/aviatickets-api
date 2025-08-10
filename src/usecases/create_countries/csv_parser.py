from typing import List

from src.dto.locations import CreateCountryDTO


class CountriesCsvParser:
    def execute(self, data: list[list[str]]) -> CreateCountryDTO:
        return [CreateCountryDTO(iso=row[0], name=row[1], name_english=row[2]) for row in data]
