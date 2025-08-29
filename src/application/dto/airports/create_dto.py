from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class CreateAirportDTO(BaseModel):
    name: str
    continent: str
    scheduled_service: str
    icao: str
    iata: str
    gps_code: str
    country_id: Optional[UUID] = None
    region_id: Optional[UUID] = None
    city_id: Optional[UUID] = None
    municipality: Optional[str] = None
    name_russian: Optional[str] = None
