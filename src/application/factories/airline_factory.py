from src.entities.airline.airline import Airline
from src.entities.airline.value_objects.iata_code import IATACode
from src.entities.airline.value_objects.icao_code import ICAOCode
from src.entities.airline.value_objects.name import AirlineName
from src.entities.airline.value_objects.name_russian import AirlineNameRussian


class AirlineFactory:
    @classmethod
    def create(cls, iata: str, icao: str, name: str, name_russian: str) -> Airline:
        return Airline.create(
            iata=IATACode(iata),
            icao=ICAOCode(icao),
            name=AirlineName(name),
            name_russian=AirlineNameRussian(name_russian),
        )
