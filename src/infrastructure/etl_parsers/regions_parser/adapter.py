from src.application.dto.location import CreateRegionDTO
from src.entities.location.country.iso import ISOCode
from src.entities.location.location_repository import LocationRepositoryInterface
from src.infrastructure.etl_parsers.regions_parser.csv_data import RegionCSVData


class RegionsLoaderAdapter:
    def __init__(self, repository: LocationRepositoryInterface) -> None:
        self.repository = repository

    async def execute(self, data: list[RegionCSVData]) -> list[CreateRegionDTO]:
        output_data = []
        for csv_data in data:
            country_iso = ISOCode(csv_data.iso.split("-")[0])

            country = await self.repository.get_country(iso=country_iso)

            region = CreateRegionDTO(
                iso=csv_data.iso,
                name=csv_data.name,
                name_english=csv_data.name_english,
                country_id=country.id.value if country else None,
            )

            output_data.append(region)

        return output_data
