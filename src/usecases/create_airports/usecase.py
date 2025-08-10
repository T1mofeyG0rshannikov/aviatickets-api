from typing import List

from src.entities.airport.iata_code import IATACode
from src.entities.airport.icao_code import ICAOCode
from src.repositories.airport_repository import AirportRepository
from src.repositories.location_repository import LocationRepository
from src.usecases.create_airports.adapter import AirportsCsvToCreateDTOAdapter
from src.usecases.create_airports.csv_parser import AirportsCsvParser


class CreateAirports:
    def __init__(
        self,
        repository: AirportRepository,
        csv_parser: AirportsCsvParser,
        adapter: AirportsCsvToCreateDTOAdapter,
        location_repository: LocationRepository,
    ) -> None:
        self.repository = repository
        self.csv_parser = csv_parser
        self.adapter = adapter
        self.location_repository = location_repository

    async def get_exist_codes(self) -> set[tuple[IATACode, ICAOCode]]:
        airports = await self.repository.all()
        return {airport.get_unique_code() for airport in airports}

    async def __call__(self, airports: list[list[str]]) -> None:
        csv_data = self.csv_parser.execute(airports)

        countries = await self.location_repository.all_countries()

        countries_dict = {country.iso: country for country in countries}

        regions = await self.location_repository.all_regions()

        regions_dict = {region.iso: region for region in regions}

        cities = await self.location_repository.all_cities()

        cities_dict = {city.name_english: city for city in cities}

        parsed_data = self.adapter.execute(
            csv_data, countries_dict=countries_dict, cities_dict=cities_dict, regions_dict=regions_dict
        )

        exist_codes = await self.get_exist_codes()
        create_data = [data for data in parsed_data if data.get_unique_code() not in exist_codes]

        return await self.repository.create_many(airports=create_data)
