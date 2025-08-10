from typing import List

from src.usecases.create_regions.dto import CsvRegionData


class RegionsCsvParser:
    def execute(self, data: list[list[str]]) -> list[CsvRegionData]:
        return [CsvRegionData(name=row[0], name_english=row[1], iso=row[2]) for row in data]
