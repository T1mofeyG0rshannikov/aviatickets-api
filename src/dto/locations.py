from dataclasses import dataclass


@dataclass
class CreateCountryDTO:
    iso: str
    name: str
    name_english: str


@dataclass
class CreateRegionDTO:
    iso: str
    name: str
    name_english: str
    country_id: int


@dataclass
class CreateCityDTO:
    name: str
    name_english: str
