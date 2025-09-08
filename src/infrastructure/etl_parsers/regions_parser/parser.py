from src.application.dto.location import CreateRegionDTO
from src.application.usecases.region.import_regions.loader import RegionsLoader
from src.infrastructure.etl_parsers.regions_parser.adapter import RegionsLoaderAdapter
from src.infrastructure.etl_parsers.regions_parser.csv_data import RegionCSVData


class RegionsCsvParser(RegionsLoader):
    def __init__(self, data: list[list[str]], adapter: RegionsLoaderAdapter) -> None:
        self._data = data
        self.adapter = adapter

    async def load(self) -> list[CreateRegionDTO]:
        csv_data = [RegionCSVData(name=row[0], name_english=row[1], iso=row[2]) for row in self._data]

        return await self.adapter.execute(csv_data)
