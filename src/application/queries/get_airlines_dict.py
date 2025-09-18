from typing import Any, Literal

from src.entities.airline.airline import Airline
from src.entities.airline.airline_repository import AirlineRepositoryInterface
from src.entities.airline.value_objects.iata_code import IATACode
from src.entities.value_objects.entity_id import EntityId


class GetAirlinesDict:
    def __init__(self, repository: AirlineRepositoryInterface):
        self.repository = repository

    async def __call__(self, codes: set[IATACode], key: Literal["iata", "id"]) -> dict[EntityId, Airline]:
        airlines = await self.repository.filter(codes)

        airlines_dict: dict[Any, Airline] = {}

        if key == "iata":

            def key_func(a):
                return a.iata

        elif key == "id":

            def key_func(a):
                return a.id

        else:
            raise ValueError(f"invalid key - '{key}'")

        for airline in airlines:
            airlines_dict[key_func(airline)] = airline
        print(airlines_dict)
        return airlines_dict
