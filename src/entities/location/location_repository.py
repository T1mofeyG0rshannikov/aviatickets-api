from typing import Protocol

from src.entities.location.city.city import City
from src.entities.location.country.country import Country
from src.entities.location.region.region import Region


class LocationRepositoryInterface(Protocol):
    async def all_cities(self) -> list[City]:
        raise NotImplementedError

    async def get_city(self, name_english: str) -> City:
        raise NotImplementedError

    async def save_cities(self, cities: list[City]) -> None:
        raise NotImplementedError

    async def get_region(self, iso: str) -> Region:
        raise NotImplementedError

    async def get_country(self, iso: str) -> Country:
        raise NotImplementedError

    async def all_countries(self) -> list[Country]:
        raise NotImplementedError

    async def all_regions(self) -> list[Region]:
        raise NotImplementedError

    async def create_countries(self, countries: list[Country]) -> None:
        raise NotImplementedError

    async def create_regions(self, regions: list[Region]) -> None:
        raise NotImplementedError
