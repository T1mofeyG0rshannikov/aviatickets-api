from typing import Any, Literal

from avia.entities.aircraft.entity import Aircraft
from avia.entities.aircraft.repository import AircraftRepositoryInterface
from avia.entities.aircraft.value_objects.iata import IATACode


class GetAircraftsDict:
    def __init__(self, repository: AircraftRepositoryInterface):
        self.repository = repository

    async def __call__(self, codes: set[IATACode], key: Literal["iata", "id"]) -> dict[Any, Aircraft]:
        aircrafts = await self.repository.filter(codes)

        aircrfts_dict: dict[Any, Aircraft] = {}

        if key == "iata":

            def key_func(a):
                return a.iata.value

        elif key == "id":

            def key_func(a):
                return a.id.value

        else:
            raise ValueError(f"invalid key - '{key}'")

        for aircraft in aircrafts:
            aircrfts_dict[key_func(aircraft)] = aircraft

        return aircrfts_dict
