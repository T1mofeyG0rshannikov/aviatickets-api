from pydantic import BaseModel


class RegionCSVData(BaseModel):
    name: str
    name_english: str
    iso: str