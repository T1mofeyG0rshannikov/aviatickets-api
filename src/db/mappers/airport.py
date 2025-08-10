from src.db.models.models import AirportOrm
from src.entities.airport.airport import Airport


def orm_to_airport(airport: AirportOrm) -> Airport:
    return Airport(
        id=airport.id,
        name=airport.name,
        continent=airport.continent,
        country_id=airport.country_id,
        region_id=airport.region_id,
        city_id=airport.city_id,
        scheduled_service=airport.scheduled_service,
        icao=airport.icao,
        iata=airport.iata,
        gps_code=airport.gps_code,
        name_russian=airport.name_russian,
    )
