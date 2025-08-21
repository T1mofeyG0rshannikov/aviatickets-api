from sqlalchemy import select

from src.entities.city.city import City
from src.entities.city.dto import CreateCityDTO
from src.entities.country.country import Country
from src.entities.country.dto import CreateCountryDTO
from src.entities.region.dto import CreateRegionDTO
from src.entities.region.region import Region
from src.infrastructure.db.mappers.city import orm_to_city
from src.infrastructure.db.mappers.country import orm_to_country
from src.infrastructure.db.mappers.region import orm_to_region
from src.infrastructure.db.models.models import CityOrm, CountryOrm, RegionOrm
from src.infrastructure.repositories.base_repository import BaseRepository


class LocationRepository(BaseRepository):
    async def all_cities(self) -> list[City]:
        results = await self.db.execute(select(CityOrm))
        cities = results.scalars().all()

        return [orm_to_city(city) for city in cities]

    async def get_city(self, name_english: str) -> City:
        result = await self.db.execute(select(CityOrm).where(CityOrm.name_english == name_english))
        city = result.scalar()
        return orm_to_city(city)

    async def create_cities(self, cities: list[CreateCityDTO]) -> None:
        cities_orm = [CityOrm(name=city.name, name_english=city.name_english) for city in cities]

        self.db.add_all(cities_orm)
        await self.db.commit()

    async def get_region(self, iso: str) -> Region:
        result = await self.db.execute(select(RegionOrm).where(RegionOrm.iso == iso))
        region = result.scalar()
        return orm_to_region(region)

    async def get_country(self, iso: str) -> Country:
        result = await self.db.execute(select(CountryOrm).where(CountryOrm.iso == iso))
        country = result.scalar()
        return orm_to_country(country) if country else None

    async def all_countries(self) -> list[Country]:
        results = await self.db.execute(select(CountryOrm))
        countries = results.scalars().all()
        return [orm_to_country(country) for country in countries]

    async def all_regions(self) -> list[Region]:
        results = await self.db.execute(select(RegionOrm))
        regions = results.scalars().all()

        return [orm_to_region(region) for region in regions]

    async def create_countries(self, countries: list[CreateCountryDTO]) -> None:
        countries_orm = [
            CountryOrm(iso=country.iso, name=country.name, name_english=country.name_english) for country in countries
        ]

        self.db.add_all(countries_orm)
        await self.db.commit()

    async def create_regions(self, regions: list[CreateRegionDTO]) -> None:
        regions_orm = [
            RegionOrm(iso=region.iso, name=region.name, name_english=region.name_english, country_id=region.country_id)
            for region in regions
        ]

        self.db.add_all(regions_orm)
        await self.db.commit()
