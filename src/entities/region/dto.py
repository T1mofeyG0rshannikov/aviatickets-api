from dataclasses import dataclass

from src.entities.region.iso import ISOCode


@dataclass
class CreateRegionDTO:
    iso: ISOCode
    name: str
    name_english: str
    country_id: int

    def __post__init__(self) -> None:
        if not isinstance(self.iso, ISOCode):
            self.iso = ISOCode(self.iso)
