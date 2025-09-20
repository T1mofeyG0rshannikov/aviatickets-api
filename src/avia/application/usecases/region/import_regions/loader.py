from abc import ABC, abstractmethod

from avia.application.dto.location import CreateRegionDTO


class RegionsLoader(ABC):
    @abstractmethod
    async def load(self) -> list[CreateRegionDTO]:
        ...
