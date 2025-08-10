from src.db.models.models import AirlineOrm
from src.entities.airline.airline import Airline


def from_orm_to_airline(airline: AirlineOrm) -> Airline:
    return Airline(
        id=airline.id, iata=airline.iata, icao=airline.icao, name=airline.name, name_russian=airline.name_russian
    )
