from dataclasses import dataclass

from src.entities.country.iso import ISOCode


@dataclass
class Country:
    id: int
    iso: ISOCode
    name: str
    name_english: str
