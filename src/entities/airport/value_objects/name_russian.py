import re
from dataclasses import dataclass

from src.entities.airport.exception import InvalidAirportNameRussianError


@dataclass(frozen=True)
class AirportNameRussian:
    """
    Value Object for airport russian name
    """

    value: str

    def validation(self, value: str):
        pattern = re.compile(r"[а-яА-ЯёЁ]")
        return bool(pattern.search(value))

    def __post_init__(self):
        if not self.validation(self.value):
            raise InvalidAirportNameRussianError(f"{self.value} is not valid airport russian name")
