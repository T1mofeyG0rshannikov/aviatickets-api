import pycountry

from avia.application.persistence.bulk_savers.country_saver import (
    CountryBulkSaverInterface,
)
from avia.entities.location.country.country import Country
from avia.entities.location.country.iso import ISOCode
from avia.entities.location.location_repository import LocationRepositoryInterface


class GetOrCreateCountriesByISO:
    def __init__(self, saver: CountryBulkSaverInterface, location_repository: LocationRepositoryInterface) -> None:
        self.saver = saver
        self.location_repository = location_repository

    async def __call__(self, codes: set[ISOCode]) -> dict[ISOCode, Country]:
        countries_from_db = await self.location_repository.all_countries()
        countries_from_db_dict = {country.iso: country for country in countries_from_db}

        countries_dict = dict()
        countries_to_save: set[Country] = set()

        for country_iso in codes:
            country_from_db = countries_from_db_dict.get(country_iso)

            if country_from_db is None:
                pyc_country = pycountry.subdivisions.get(code=country_iso)
                if pyc_country is not None:
                    country = Country.create(iso=pyc_country.code, name_english=pyc_country.name)  # type: ignore

                    countries_to_save.add(country)

                    countries_dict[country_iso] = country

            else:
                countries_dict[country_iso] = country_from_db

        await self.saver.add_many(list(countries_to_save))
        return countries_dict
