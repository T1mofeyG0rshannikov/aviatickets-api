import json
from typing import Any

import pycountry
from redis import Redis  # type: ignore

from avia.application.persistence.bulk_savers.country_saver import (
    CountryBulkSaverInterface,
)
from avia.entities.location.country.country import Country
from avia.entities.location.country.iso import ISOCode
from avia.entities.location.location_repository import LocationRepositoryInterface


class GetOrCreateCountriesByISO:
    def __init__(
        self,
        saver: CountryBulkSaverInterface,
        location_repository: LocationRepositoryInterface,
        redis: Redis,
        cache_key: str = "pycountry_cache",
    ) -> None:
        self.saver = saver
        self.location_repository = location_repository
        self._cache_key = cache_key
        self._redis = redis

    def get_data(self) -> dict[str, Any]:
        pycountry_cache = self._redis.get(self._cache_key)
        if pycountry_cache is None:
            pycountry_data = {
                obj.code: {"name": str(obj.name), "code": str(obj.code)} for obj in pycountry.subdivisions
            }
            self._redis.set(self._cache_key, json.dumps(pycountry_data))

            return pycountry_data

        return json.loads(pycountry_cache)

    async def __call__(self, codes: set[ISOCode]) -> dict[ISOCode, Country]:
        countries_from_db = await self.location_repository.all_countries()
        countries_from_db_dict = {country.iso: country for country in countries_from_db}

        countries_dict = dict()
        countries_to_save: set[Country] = set()

        data = self.get_data()

        for country_iso in codes:
            country_from_db = countries_from_db_dict.get(country_iso)

            if country_from_db is None:
                pyc_country = data.get(country_iso)
                if pyc_country is not None:
                    country = Country.create(iso=pyc_country.code, name_english=pyc_country.name)  # type: ignore

                    countries_to_save.add(country)

                    countries_dict[country_iso] = country

            else:
                countries_dict[country_iso] = country_from_db

        await self.saver.add_many(list(countries_to_save))
        return countries_dict
