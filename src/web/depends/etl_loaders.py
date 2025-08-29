from typing import Annotated

from fastapi import Depends
from src.infrastructure.etl_parsers.airlines_parser import AirlinesTXTParser
from src.infrastructure.depends.base import get_csv_to_airport_adapter
from src.infrastructure.etl_parsers.airports_parser.adapter import CsvToAirportAdapter
from src.infrastructure.etl_parsers.airports_parser.airports_parser import AirportsCsvParser
from src.infrastructure.etl_parsers.regions_parser.parser import RegionsCsvParser
from src.infrastructure.etl_parsers.regions_parser.adapter import RegionsLoaderAdapter
from src.infrastructure.etl_parsers.cities_parser import CitiesCsvParser
from src.infrastructure.etl_parsers.countries_parser import CountriesCsvParser
from src.web.depends.files_from_request import get_csv_file, get_txt_file
from src.web.depends.annotations.annotations import LocationRepositoryAnnotation


def get_countries_csv_parser(
    csv_data: Annotated[list[list[str]], Depends(get_csv_file)],
) -> CountriesCsvParser:
    return CountriesCsvParser(csv_data)


def get_cities_csv_parser(
    csv_data: Annotated[list[list[str]], Depends(get_csv_file)],
) -> CitiesCsvParser:
    return CitiesCsvParser(csv_data)


def get_regions_loader_adapter(repository: LocationRepositoryAnnotation) -> RegionsLoaderAdapter:
    return RegionsLoaderAdapter(repository)


def get_regions_csv_parser(
    csv_data: Annotated[list[list[str]], Depends(get_csv_file)],
    adapter: Annotated[RegionsLoaderAdapter, Depends(get_regions_loader_adapter)],
) -> RegionsCsvParser:
    return RegionsCsvParser(csv_data, adapter)


def get_csv_airports_parser(
    csv_data: Annotated[list[list[str]], Depends(get_csv_file)],
    adapter: Annotated[CsvToAirportAdapter, Depends(get_csv_to_airport_adapter)],
    location_repository: LocationRepositoryAnnotation,
) -> AirportsCsvParser:
    return AirportsCsvParser(csv_data, adapter, location_repository)


def get_txt_airlines_parser(
    txt_data: Annotated[list[str], Depends(get_txt_file)],
) -> AirlinesTXTParser:
    return AirlinesTXTParser(txt_data)