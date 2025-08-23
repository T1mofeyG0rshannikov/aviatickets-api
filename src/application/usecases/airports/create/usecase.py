from src.application.dto.bulk_result import BulkResult
from src.application.usecases.airports.airport_importer import AirportImporterInterface
from src.application.usecases.airports.create.adapter import CsvToAirportAdapter
from src.application.usecases.airports.create.csv_parser import AirportsCsvParser
from src.entities.airport.airport import Airport
from src.entities.airport.airport_repository import AirportRepositoryInterface
from src.entities.airport.iata_code import IATACode
from src.entities.airport.icao_code import ICAOCode
from src.entities.location.location_repository import LocationRepositoryInterface


class CreateAirports:
    def __init__(
        self,
        repository: AirportRepositoryInterface,
        importer: AirportImporterInterface,
        csv_parser: AirportsCsvParser,
        adapter: CsvToAirportAdapter,
        location_repository: LocationRepositoryInterface,
    ) -> None:
        self.repository = repository
        self.location_repository = location_repository
        self.importer = importer
        self.csv_parser = csv_parser
        self.adapter = adapter

    async def get_exist_codes(self) -> set[tuple[IATACode, ICAOCode]]:
        airports = await self.repository.all()
        return {airport.iata for airport in airports}

    async def __call__(self, airports: list[list[str]]) -> BulkResult:
        csv_data = self.csv_parser.execute(airports)

        skipped = 0

        airports: list[Airport] = []

        countries = await self.location_repository.all_countries()

        countries_dict = {country.iso: country for country in countries}

        regions = await self.location_repository.all_regions()

        regions_dict = {region.iso: region for region in regions}

        cities = await self.location_repository.all_cities()

        cities_dict = {city.name_english: city for city in cities}

        adapter_response = await self.adapter.execute(
            csv_data, countries_dict=countries_dict, regions_dict=regions_dict, cities_dict=cities_dict
        )

        airports = adapter_response.airports
        invalid = adapter_response.invalid

        create_data: list[Airport] = []

        exist_codes = await self.get_exist_codes()

        for airport in airports:
            if airport.iata in exist_codes:
                skipped += 1
            else:
                create_data.append(airport)

        inserted = await self.importer.create_many(airports=create_data)

        return BulkResult(skipped=skipped, inserted=inserted, invalid=invalid)
