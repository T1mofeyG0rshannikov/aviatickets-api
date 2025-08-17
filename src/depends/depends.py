from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from src.admin.config import AdminConfig
from src.depends.annotations.annotations import (
    AirlineRepositoryAnnotation,
    AirportRepositoryAnnotation,
    LocationRepositoryAnnotation,
    TicketReadRepositoryAnnotation,
    UserRepositoryAnnotation,
    UserTicketRepositoryAnnotation,
)
from src.infrastructure.email_sender.config import EmailSenderConfig
from src.infrastructure.email_sender.service import EmailSender
from src.infrastructure.jwt.jwt_config import JwtConfig
from src.infrastructure.jwt.jwt_processor import JwtProcessor
from src.infrastructure.pdf_service.service import PdfService
from src.infrastructure.security.password_hasher import PasswordHasher
from src.usecases.create_airlines.txt_parser import AirlinesTXTParser
from src.usecases.create_airports.adapter import AirportsCsvToCreateDTOAdapter
from src.usecases.create_airports.usecase import AirportsCsvParser
from src.usecases.create_cities.csv_parser import CitiesCsvParser
from src.usecases.create_countries.csv_parser import CountriesCsvParser
from src.usecases.create_regions.adapter import RegionCsvToCreateDTOAdapter
from src.usecases.create_regions.csv_parser import RegionsCsvParser
from src.usecases.tickets.parse.parsers.aviasales.config import AviasalesAPIConfig
from src.usecases.tickets.parse.parsers.aviasales.parser import AviasalesTicketParser
from src.usecases.tickets.pdf.adapter import PdfTicketAdapter
from src.usecases.tickets.pdf.usecase import UserTicketFullInfoAssembler


@lru_cache
def get_jwt_config() -> JwtConfig:
    return JwtConfig()


@lru_cache
def get_password_hasher() -> PasswordHasher:
    return PasswordHasher()


def get_jwt_processor(config: Annotated[JwtConfig, Depends(get_jwt_config)]) -> JwtProcessor:
    return JwtProcessor(config)


def get_csv_airports_parser() -> AirportsCsvParser:
    return AirportsCsvParser()


def get_airports_scv_to_dto_adapter() -> AirportsCsvToCreateDTOAdapter:
    return AirportsCsvToCreateDTOAdapter()


def get_txt_airlines_parser() -> AirlinesTXTParser:
    return AirlinesTXTParser()


def get_countries_csv_parser() -> CountriesCsvParser:
    return CountriesCsvParser()


def get_regions_csv_parser() -> RegionsCsvParser:
    return RegionsCsvParser()


def get_regions_csv_to_create_adapter(repository: LocationRepositoryAnnotation) -> RegionCsvToCreateDTOAdapter:
    return RegionCsvToCreateDTOAdapter(repository)


def get_cities_csv_parser() -> CitiesCsvParser:
    return CitiesCsvParser()


@lru_cache
def get_admin_config() -> AdminConfig:
    return AdminConfig()


def get_aviasales_ticket_parser_config() -> AviasalesAPIConfig:
    return AviasalesAPIConfig()


def get_aviasales_ticket_parser(
    config: Annotated[AviasalesAPIConfig, Depends(get_aviasales_ticket_parser_config)],
    repository: AirportRepositoryAnnotation,
    airline_repository: AirlineRepositoryAnnotation,
) -> AviasalesTicketParser:
    return AviasalesTicketParser(config, repository, airline_repository)


def get_pdf_ticket_adapter() -> PdfTicketAdapter:
    return PdfTicketAdapter()


def get_user_ticket_assembler(
    user_repository: UserRepositoryAnnotation,
    ticket_repository: TicketReadRepositoryAnnotation,
    user_ticket_repository: UserTicketRepositoryAnnotation,
) -> UserTicketFullInfoAssembler:
    return UserTicketFullInfoAssembler(
        user_repository,
        ticket_repository,
        user_ticket_repository,
    )


def get_pdf_service() -> PdfService:
    return PdfService()


@lru_cache
def get_email_config() -> EmailSenderConfig:
    return EmailSenderConfig()


def get_email_sender(config: Annotated[EmailSenderConfig, Depends(get_email_config)]) -> EmailSender:
    return EmailSender(config)
