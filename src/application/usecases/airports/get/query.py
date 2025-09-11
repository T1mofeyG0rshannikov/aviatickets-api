from collections.abc import Iterable
from typing import Any

from src.entities.airport.airport import Airport
from src.entities.airport.airport_repository import AirportRepositoryInterface
from src.entities.airport.value_objects.iata_code import IATACode
from src.entities.value_objects.entity_id import EntityId


class GetAirportsDict:
    def __init__(self, airport_repository: AirportRepositoryInterface):
        self.airport_repository = airport_repository

    async def __call__(self, codes: Iterable[IATACode], key) -> dict[EntityId, Airport]:
        airports = await self.airport_repository.filter(codes)

        airports_dict: dict[Any, Airport] = {}

        if isinstance(key, IATACode):

            def key_func(airport):
                return airport.iata

        elif isinstance(key, EntityId):

            def key_func(airport):
                return airport.id

        for airport in airports:
            airports_dict[key_func] = airport

        return airports_dict
