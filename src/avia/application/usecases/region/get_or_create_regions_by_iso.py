import json
from typing import Any

import pycountry
from redis import Redis  # type: ignore

from avia.application.persistence.bulk_savers.region_saver import (
    RegionBulkSaverInterface,
)
from avia.entities.location.country.country import Country
from avia.entities.location.country.iso import ISOCode as CountryISOCode
from avia.entities.location.location_repository import LocationRepositoryInterface
from avia.entities.location.region.iso import ISOCode
from avia.entities.location.region.region import Region


class GetOrCreateRegionsByISO:
    def __init__(
        self,
        regions_bulk_saver: RegionBulkSaverInterface,
        location_repository: LocationRepositoryInterface,
        redis: Redis,
        cache_key: str = "pycountry_cache",
    ) -> None:
        self.saver = regions_bulk_saver
        self.location_repository = location_repository
        self.location_repository = location_repository
        self._cache_key = cache_key
        self._redis = redis

    def get_data(self) -> dict[str, Any]:
        pycountry_cache = self._redis.get(self._cache_key)
        if pycountry_cache is None:
            pycountry_data = {obj.code: {"name": obj.name, "code": obj.code} for obj in pycountry.subdivisions}
            self._redis.set(pycountry_cache, json.dumps(pycountry_data))

            return pycountry_data

        return json.loads(pycountry_cache)

    async def __call__(
        self, codes: set[ISOCode], countries_dict: dict[CountryISOCode, Country]
    ) -> dict[ISOCode, Region]:
        regions_from_db = await self.location_repository.all_regions()
        regions_from_db_dict = {region.iso: region for region in regions_from_db}

        regions_dict = dict()
        regions_to_save = set()

        data = self.get_data()

        for region_iso in codes:
            region_from_db = regions_from_db_dict.get(region_iso)

            if region_from_db is None:
                pyc_region = data.get(region_iso)
                print(region_iso, pyc_region)
                if pyc_region is not None:
                    region = Region.create(
                        iso=ISOCode(pyc_region.code),
                        name=None,  # type: ignore
                        name_english=pyc_region.name,
                        country_id=countries_dict[region_iso.split("-")[0]].id,  # type: ignore
                    )

                    regions_to_save.add(region)

                    regions_dict[region_iso] = region

            else:
                regions_dict[region_iso] = region_from_db

        await self.saver.add_many(list(regions_to_save))
        return regions_dict
