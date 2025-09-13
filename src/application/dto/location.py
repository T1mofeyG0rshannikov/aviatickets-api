from dataclasses import dataclass
from uuid import UUID

from pydantic import BaseModel


@dataclass
class CityDTO:
    id: UUID
    name: str
    name_english: str


@dataclass
class CityWithAirportsDTO:
    id: UUID
    name: str
    name_english: str
    airports: list[UUID]


class CreateCityDTO(BaseModel):
    name: str
    name_english: str


class CreateCountryDTO(BaseModel):
    iso: str
    name: str
    name_english: str


@dataclass
class CountryDTO:
    id: UUID
    iso: str
    name: str
    name_english: str


@dataclass
class CountryWithAirportsDTO:
    id: UUID
    iso: str
    name: str
    name_english: str
    airports: list[UUID]


@dataclass
class RegionDTO:
    id: UUID
    iso: str
    name: str
    name_english: str


class CreateRegionDTO(BaseModel):
    name: str
    name_english: str
    iso: str
    country_id: UUID
