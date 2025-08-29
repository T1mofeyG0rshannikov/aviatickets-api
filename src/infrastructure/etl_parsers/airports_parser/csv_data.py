from typing import Optional
from pydantic import BaseModel


class AirportCSVData(BaseModel):
    name: str
    continent: str
    iso_country: str
    iso_region: str
    municipality: str
    scheduled_service: str
    icao: str
    iata: str
    gps_code: str
    name_russian: Optional[str]
