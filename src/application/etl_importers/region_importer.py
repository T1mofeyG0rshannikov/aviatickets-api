from abc import ABC, abstractmethod

from src.entities.location.region.region import Region


class RegionImporterInterface(ABC):
    @abstractmethod
    async def add_many(self, regions: list[Region]) -> int:
        ...
