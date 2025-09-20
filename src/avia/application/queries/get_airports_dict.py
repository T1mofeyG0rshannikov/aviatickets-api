from collections.abc import Iterable
from typing import Any, Literal

from avia.entities.airport.airport import Airport
from avia.entities.airport.airport_repository import AirportRepositoryInterface
from avia.entities.airport.value_objects.iata_code import IATACode


class GetAirportsDict:
    def __init__(self, airport_repository: AirportRepositoryInterface):
        self.airport_repository = airport_repository

    async def __call__(self, codes: Iterable[IATACode], key: Literal["iata", "id"]) -> dict[Any, Airport]:
        airports = await self.airport_repository.filter(codes)

        airports_dict: dict[Any, Airport] = {}

        if key == "iata":

            def key_func(a):
                return a.iata

        elif key == "id":

            def key_func(a):
                return a.id

        else:
            raise ValueError(f"invalid key - '{key}'")

        for airport in airports:
            airports_dict[key_func(airport)] = airport
        return airports_dict
