from src.application.usecases.create_regions.dto import CsvRegionData
from src.entities.location.location_repository import LocationRepositoryInterface
from src.entities.location.region.region import Region


class RegionCsvToEntitiesAdapter:
    def __init__(self, repository: LocationRepositoryInterface) -> None:
        self.repository = repository

    async def execute(self, data: list[CsvRegionData]) -> list[Region]:
        output_data = []

        for csv_data in data:
            country_iso = csv_data.iso.split("-")[0]

            country = await self.repository.get_country(iso=country_iso)

            try:
                region = Region.create(
                    iso=csv_data.iso,
                    name=csv_data.name,
                    name_english=csv_data.name_english,
                    country_id=country.id if country else None,
                )

                output_data.append(region)
            except ValueError:
                pass

        return output_data
