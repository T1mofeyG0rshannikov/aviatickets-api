from src.application.dto.airports.create_dto import CreateAirportDTO
from src.application.usecases.airports.create.loader import (
    AirportsLoader,
    AirportsLoaderResponse,
)
from src.infrastructure.etl_parsers.airports_parser.adapter import CsvToAirportAdapter
from src.infrastructure.etl_parsers.airports_parser.csv_data import AirportCSVData
from src.infrastructure.persistence.repositories.location_repository import (
    LocationRepository,
)


class AirportsCsvParser(AirportsLoader):
    def __init__(
        self, data: list[list[str]], adapter: CsvToAirportAdapter, location_repository: LocationRepository
    ) -> None:
        self._data = data
        self.adapter = adapter
        self.location_repository = location_repository

    def get_russian_name(self, keywords: str) -> str | None:
        try:
            return keywords.split(", ")[1]
        except:
            return None

    async def load(self) -> AirportsLoaderResponse:
        csv_data = [
            AirportCSVData(
                name=row[3],
                continent=row[7],
                iso_country=row[8],
                iso_region=row[9],
                municipality=row[10],
                scheduled_service=row[11],
                icao=row[12],
                iata=row[13],
                gps_code=row[14],
                name_russian=self.get_russian_name(row[18]),
            )
            for row in self._data
        ]
        countries = await self.location_repository.all_countries()

        countries_dict = {country.iso: country for country in countries}

        regions = await self.location_repository.all_regions()

        regions_dict = {region.iso: region for region in regions}

        cities = await self.location_repository.all_cities()

        cities_dict = {city.name_english: city for city in cities}

        return await self.adapter.execute(
            csv_data, countries_dict=countries_dict, regions_dict=regions_dict, cities_dict=cities_dict
        )
