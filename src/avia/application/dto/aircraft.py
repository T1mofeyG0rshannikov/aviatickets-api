from dataclasses import dataclass


@dataclass
class CreateAircraftDTO:
    iata: str
    name: str
    wtc: str


@dataclass
class AircraftDTO:
    name: str
    iata: str
