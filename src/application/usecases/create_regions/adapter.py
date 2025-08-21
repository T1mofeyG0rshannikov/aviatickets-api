from src.application.usecases.create_regions.dto import CsvRegionData
from src.entities.region.dto import CreateRegionDTO
from src.entities.region.iso import ISOCode
from src.infrastructure.repositories.location_repository import LocationRepository


class RegionCsvToCreateDTOAdapter:
    def __init__(self, repository: LocationRepository) -> None:
        self.repository = repository

    async def execute(self, data: list[CsvRegionData]) -> list[CreateRegionDTO]:
        output_data = []

        for csv_data in data:
            country_iso = csv_data.iso.split("-")[0]

            country = await self.repository.get_country(iso=country_iso)

            output_data.append(
                CreateRegionDTO(
                    iso=csv_data.iso,
                    name=csv_data.name,
                    name_english=csv_data.name_english,
                    country_id=country.id if country else None,
                )
            )

        return output_data
