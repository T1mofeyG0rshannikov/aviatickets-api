from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from src.admin.config import AdminConfig
from src.depends.annotations.annotations import (
    AirlineRepositoryAnnotation,
    AirportRepositoryAnnotation,
    LocationRepositoryAnnotation,
    TicketReadRepositoryAnnotation,
    TicketRepositoryAnnotation,
)
from src.depends.annotations.db_annotation import DbAnnotation
from src.repositories.user_repository import UserRepository
from src.usecases.create_airlines.txt_parser import AirlinesTXTParser
from src.usecases.create_airlines.usecase import CreateAirlines
from src.usecases.create_airports.adapter import AirportsCsvToCreateDTOAdapter
from src.usecases.create_airports.usecase import AirportsCsvParser, CreateAirports
from src.usecases.create_cities.csv_parser import CitiesCsvParser
from src.usecases.create_cities.usecase import CreateCities
from src.usecases.create_countries.csv_parser import CountriesCsvParser
from src.usecases.create_countries.usecase import CreateCountries
from src.usecases.create_regions.adapter import RegionCsvToCreateDTOAdapter
from src.usecases.create_regions.csv_parser import RegionsCsvParser
from src.usecases.create_regions.usecase import CreateRegions
from src.usecases.tickets.filter.usecase import FilterTickets
from src.usecases.tickets.parse.parsers.aviasales.config import AviasalesAPIConfig
from src.usecases.tickets.parse.parsers.aviasales.parser import AviasalesTicketParser
from src.usecases.tickets.parse.usecase import ParseAviaTickets
from src.user.auth.jwt_config import JwtConfig
from src.user.auth.jwt_processor import JwtProcessor
from src.user.password_hasher import PasswordHasher


@lru_cache
def get_jwt_config() -> JwtConfig:
    return JwtConfig()


@lru_cache
def get_password_hasher() -> PasswordHasher:
    return PasswordHasher()


def get_jwt_processor(config: JwtConfig = get_jwt_config()) -> JwtProcessor:
    return JwtProcessor(config)


def get_csv_airports_parser() -> AirportsCsvParser:
    return AirportsCsvParser()


def get_airports_scv_to_dto_adapter() -> AirportsCsvToCreateDTOAdapter:
    return AirportsCsvToCreateDTOAdapter()


def get_create_airports_interactor(
    repository: AirportRepositoryAnnotation,
    csv_parser: Annotated[AirportsCsvParser, Depends(get_csv_airports_parser)],
    adapter: Annotated[AirportsCsvToCreateDTOAdapter, Depends(get_airports_scv_to_dto_adapter)],
    location_repository: LocationRepositoryAnnotation,
) -> CreateAirports:
    return CreateAirports(repository, csv_parser, adapter, location_repository)


def get_txt_airlines_parser() -> AirlinesTXTParser:
    return AirlinesTXTParser()


def get_create_airlines_interactor(
    repository: AirlineRepositoryAnnotation, txt_parser: Annotated[AirlinesTXTParser, Depends(get_txt_airlines_parser)]
) -> CreateAirlines:
    return CreateAirlines(repository, txt_parser)


def get_countries_csv_parser() -> CountriesCsvParser:
    return CountriesCsvParser()


def get_create_countries_interactor(
    csv_parser: Annotated[CountriesCsvParser, Depends(get_countries_csv_parser)],
    repository: LocationRepositoryAnnotation,
) -> CreateCountries:
    return CreateCountries(csv_parser, repository)


def get_regions_csv_parser() -> RegionsCsvParser:
    return RegionsCsvParser()


def get_regions_csv_to_create_adapter(repository: LocationRepositoryAnnotation) -> RegionCsvToCreateDTOAdapter:
    return RegionCsvToCreateDTOAdapter(repository)


def get_create_regions_interactor(
    csv_parser: Annotated[RegionsCsvParser, Depends(get_regions_csv_parser)],
    repository: LocationRepositoryAnnotation,
    adapter: Annotated[RegionCsvToCreateDTOAdapter, Depends(get_regions_csv_to_create_adapter)],
) -> CreateRegions:
    return CreateRegions(csv_parser=csv_parser, repository=repository, adapter=adapter)


def get_cities_csv_parser() -> CitiesCsvParser:
    return CitiesCsvParser()


def get_create_cities_interactor(
    csv_parser: Annotated[CitiesCsvParser, Depends(get_cities_csv_parser)],
    repository: LocationRepositoryAnnotation,
) -> CreateCities:
    return CreateCities(
        csv_parser=csv_parser,
        repository=repository,
    )


@lru_cache
def get_admin_config() -> AdminConfig:
    return AdminConfig()


def get_user_repository(db: DbAnnotation) -> UserRepository:
    return UserRepository(db)


def get_aviasales_ticket_parser_config() -> AviasalesAPIConfig:
    return AviasalesAPIConfig()


def get_aviasales_ticket_parser(
    config: Annotated[AviasalesAPIConfig, Depends(get_aviasales_ticket_parser_config)],
    repository: AirportRepositoryAnnotation,
    airline_repository: AirlineRepositoryAnnotation,
) -> AviasalesTicketParser:
    return AviasalesTicketParser(config, repository, airline_repository)


def get_parse_tickets_interactor(
    aviasales_parser: Annotated[AviasalesTicketParser, Depends(get_aviasales_ticket_parser)],
    airports_repository: AirportRepositoryAnnotation,
    ticket_repository: TicketRepositoryAnnotation,
) -> ParseAviaTickets:
    return ParseAviaTickets(
        parsers=[aviasales_parser], airports_repository=airports_repository, ticket_repository=ticket_repository
    )


def get_filter_tickets_interactor(ticket_repository: TicketReadRepositoryAnnotation) -> FilterTickets:
    return FilterTickets(ticket_repository)
