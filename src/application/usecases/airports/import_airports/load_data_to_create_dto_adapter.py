from src.application.usecases.airports.import_airports.adapter import (
    AirportLoadDataToCreateDTOAdapter,
    AirportsAdapterResponse,
)
from src.application.usecases.airports.import_airports.load_data import AirportLoadData
from src.application.usecases.country.get_or_create_countries_by_iso import (
    GetOrCreateCountriesByISO,
)
from src.application.usecases.region.get_or_create_regions_by_iso import (
    GetOrCreateRegionsByISO,
)
from src.entities.exceptions import DomainError
from src.entities.location.country.iso import ISOCode as CountryISO
from src.entities.location.location_repository import LocationRepositoryInterface
from src.entities.location.region.iso import ISOCode as RegionISO


class ConvertAirportLoadDataToCreateData:
    def __init__(
        self,
        location_repository: LocationRepositoryInterface,
        adapter: AirportLoadDataToCreateDTOAdapter,
        get_or_create_countries_by_iso: GetOrCreateCountriesByISO,
        get_or_create_regions_by_iso: GetOrCreateRegionsByISO,
    ) -> None:
        self.location_repository = location_repository
        self.adapter = adapter
        self.get_or_create_countries_by_iso = get_or_create_countries_by_iso
        self.get_or_create_regions_by_iso = get_or_create_regions_by_iso

    async def __call__(self, airports: list[AirportLoadData]) -> AirportsAdapterResponse:
        regions_iso = set()
        countries_iso = set()

        for load_data in airports:
            try:
                regions_iso.add(RegionISO(load_data.region_iso))
            except DomainError as e:
                print(f"Error while building region iso: {e}")

            try:
                countries_iso.add(CountryISO(load_data.country_iso))
            except DomainError as e:
                print(f"Error while building country iso: {e}")

        countries_dict = await self.get_or_create_countries_by_iso(countries_iso)

        regions_dict = await self.get_or_create_regions_by_iso(regions_iso, countries_dict)

        cities = await self.location_repository.all_cities()

        cities_dict = {city.name_english: city for city in cities}

        return await self.adapter.execute(
            data=airports, countries_dict=countries_dict, regions_dict=regions_dict, cities_dict=cities_dict
        )
