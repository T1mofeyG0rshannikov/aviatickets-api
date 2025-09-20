from abc import ABC, abstractmethod

from avia.entities.location.region.region import Region


class RegionBulkSaverInterface(ABC):
    @abstractmethod
    async def add_many(self, regions: list[Region]) -> int:
        ...
