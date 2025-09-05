from uuid import UUID

from pydantic import BaseModel


class CreateAirportDTO(BaseModel):
    name: str
    continent: str
    scheduled_service: str
    icao: str
    iata: str
    gps_code: str
    city_id: UUID
    country_id: UUID
    region_id: UUID
    municipality: str | None = None
    name_russian: str | None = None
