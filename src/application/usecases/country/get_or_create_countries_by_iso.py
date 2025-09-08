import pycountry

from src.application.usecases.country.persist_countries import PersistCountries
from src.entities.location.country.country import Country
from src.entities.location.country.iso import ISOCode
from src.entities.location.location_repository import LocationRepositoryInterface


class GetOrCreateCountriesByISO:
    def __init__(self, persist_countries: PersistCountries, location_repository: LocationRepositoryInterface) -> None:
        self.persist_countries = persist_countries
        self.location_repository = location_repository

    async def __call__(self, codes: set[ISOCode]) -> dict[ISOCode, Country]:
        countries_from_db = await self.location_repository.all_countries()
        countries_from_db_dict = {country.iso: country for country in countries_from_db}

        countries_dict = dict()
        countries_to_save: set[Country] = set()

        for country_iso in codes:
            country_from_db = countries_from_db_dict.get(country_iso)

            if country_from_db is None:
                print(country_iso, "ISO")
                pyc_country = pycountry.subdivisions.get(code=country_iso)
                if pyc_country is not None:
                    print(pyc_country, "PYC")
                    country = Country.create(iso=pyc_country.code, name_english=pyc_country.name)  # type: ignore

                    countries_to_save.add(country)

                    countries_dict[country_iso] = country

            else:
                countries_dict[country_iso] = country_from_db

        await self.persist_countries(list(countries_to_save))
        return countries_dict
