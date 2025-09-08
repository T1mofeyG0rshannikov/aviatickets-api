from src.application.dto.bulk_result import BulkResult
from src.application.factories.airport_factory import AirportFactory
from src.application.persistence.etl_importers.airport_importer import (
    AirportBulkSaverInterface,
)
from src.application.persistence.transaction import Transaction
from src.application.usecases.airports.import_airports.adapter import (
    AirportLoadDataToCreateDTO,
)
from src.application.usecases.airports.import_airports.loader import AirportsLoader
from src.application.usecases.country.get_or_create_countries_by_iso import (
    GetOrCreateCountriesByISO,
)
from src.application.usecases.region.get_or_create_regions_by_iso import (
    GetOrCreateRegionsByISO,
)
from src.entities.airport.airport import Airport
from src.entities.airport.airport_repository import AirportRepositoryInterface
from src.entities.airport.value_objects.iata_code import IATACode
from src.entities.exceptions import DomainError
from src.entities.location.country.iso import ISOCode as CountryISO
from src.entities.location.location_repository import LocationRepositoryInterface
from src.entities.location.region.iso import ISOCode as RegionISO


class ImportAirports:
    def __init__(
        self,
        transaction: Transaction,
        repository: AirportRepositoryInterface,
        saver: AirportBulkSaverInterface,
        loader: AirportsLoader,
        location_repository: LocationRepositoryInterface,
        adapter: AirportLoadDataToCreateDTO,
        get_or_create_countries_by_iso: GetOrCreateCountriesByISO,
        get_or_create_regions_by_iso: GetOrCreateRegionsByISO,
    ) -> None:
        self.repository = repository
        self.location_repository = location_repository
        self.saver = saver
        self.loader = loader
        self.adapter = adapter
        self.transaction = transaction
        self.get_or_create_countries_by_iso = get_or_create_countries_by_iso
        self.get_or_create_regions_by_iso = get_or_create_regions_by_iso

    async def get_exist_codes(self) -> set[IATACode]:
        airports = await self.repository.all()
        return {airport.iata for airport in airports}

    async def __call__(self) -> BulkResult:
        skipped = 0

        loader_response = await self.loader.load()

        airports = loader_response.airports
        invalid = loader_response.invalid

        regions_iso = set()
        countries_iso = set()

        for load_data in airports:
            regions_iso.add(RegionISO(load_data.region_iso))
            countries_iso.add(CountryISO(load_data.country_iso))

        countries_dict = await self.get_or_create_countries_by_iso(countries_iso)

        regions_dict = await self.get_or_create_regions_by_iso(regions_iso, countries_dict)

        cities = await self.location_repository.all_cities()

        cities_dict = {city.name_english: city for city in cities}

        adapter_response = await self.adapter.execute(
            data=airports, countries_dict=countries_dict, regions_dict=regions_dict, cities_dict=cities_dict
        )
        create_airports_dto = adapter_response.airports
        invalid += adapter_response.invalid

        create_data: list[Airport] = []

        exist_codes = await self.get_exist_codes()

        for airport in create_airports_dto:
            if airport.iata in exist_codes:
                skipped += 1
            else:
                try:
                    create_data.append(
                        AirportFactory.create(
                            name=airport.name,
                            continent=airport.continent,
                            country_id=airport.country_id,
                            region_id=airport.region_id,
                            city_id=airport.city_id,
                            scheduled_service=airport.scheduled_service,
                            icao=airport.icao,
                            iata=airport.iata,
                            gps_code=airport.gps_code,
                            name_russian=airport.name_russian,
                        )
                    )
                except DomainError as e:
                    invalid += 1
                    print(f"Error while building Airport: {e}")
                except DomainError:
                    continue

        inserted = await self.saver.add_many(create_data)
        await self.transaction.commit()
        return BulkResult(skipped=skipped, inserted=inserted, invalid=invalid)
