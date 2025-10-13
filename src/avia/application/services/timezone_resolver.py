from abc import ABC, abstractmethod
from zoneinfo import ZoneInfo

from avia.entities.airport.value_objects.iata_code import IATACode


class TimezoneResolverInterface(ABC):
    @abstractmethod
    def get_timezone(self, iata: IATACode) -> ZoneInfo:
        ...
