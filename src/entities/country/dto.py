from dataclasses import dataclass

from src.entities.country.iso import ISOCode


@dataclass
class CreateCountryDTO:
    iso: ISOCode
    name: str
    name_english: str

    def __post__init__(self) -> None:
        if not isinstance(self.iso, ISOCode):
            self.iso = ISOCode(self.iso)
