from dataclasses import dataclass

from src.entities.region.iso import ISOCode


@dataclass
class Region:
    id: int
    iso: ISOCode
    name: str
    name_english: str
