from dataclasses import dataclass
from uuid import UUID


@dataclass
class CityDTO:
    id: UUID
    name: str
    name_english: str


@dataclass
class CountryDTO:
    id: UUID
    iso: str
    name: str
    name_english: str


@dataclass
class RegionDTO:
    id: UUID
    iso: str
    name: str
    name_english: str
