from src.entities.aircraft.entity import Aircraft
from src.entities.aircraft.value_objects.iata import IATACode
from src.entities.aircraft.value_objects.wtc import AircraftWTC


class AircraftFactory:
    @classmethod
    def create(cls, iata: str, name: str, wtc: str) -> Aircraft:
        return Aircraft.create(iata=IATACode(iata), name=name, wtc=AircraftWTC(wtc))  # type: ignore
