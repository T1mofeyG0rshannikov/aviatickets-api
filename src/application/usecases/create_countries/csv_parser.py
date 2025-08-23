from src.entities.location.country.country import Country


class CountriesCsvParser:
    def execute(self, data: list[list[str]]) -> list[Country]:
        return [Country.create(iso=row[0], name=row[1], name_english=row[2]) for row in data]
