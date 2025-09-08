import pycountry

from src.application.usecases.region.persist_regions import PersistRegions
from src.entities.location.country.country import Country
from src.entities.location.country.iso import ISOCode as CountryISOCode
from src.entities.location.location_repository import LocationRepositoryInterface
from src.entities.location.region.iso import ISOCode
from src.entities.location.region.region import Region


class GetOrCreateRegionsByISO:
    def __init__(self, persist_regions: PersistRegions, location_repository: LocationRepositoryInterface) -> None:
        self.persist_regions = persist_regions
        self.location_repository = location_repository

    async def __call__(
        self, codes: set[ISOCode], countries_dict: dict[CountryISOCode, Country]
    ) -> dict[ISOCode, Region]:
        regions_from_db = await self.location_repository.all_regions()
        regions_from_db_dict = {region.iso: region for region in regions_from_db}

        regions_dict = dict()
        regions_to_save = set()

        for region_iso in codes:
            region_from_db = regions_from_db_dict.get(region_iso)

            if region_from_db is None:
                pyc_region = pycountry.subdivisions.get(code=region_iso)
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

        await self.persist_regions(list(regions_to_save))
        return regions_dict
