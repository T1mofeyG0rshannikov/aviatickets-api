from dataclasses import dataclass


@dataclass
class AirportLoadData:
    name: str
    continent: str
    country_iso: str
    region_iso: str
    municipality: str
    scheduled_service: str
    icao: str
    iata: str
    gps_code: str
    name_russian: str | None
