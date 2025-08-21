from functools import lru_cache
from typing import Annotated

import httpx
from redis import Redis

from src.application.usecases.airports.create.adapter import (
    AirportsCsvToCreateDTOAdapter,
)
from src.application.usecases.airports.create.csv_parser import AirportsCsvParser
from src.application.usecases.create_airlines.txt_parser import AirlinesTXTParser
from src.application.usecases.create_cities.csv_parser import CitiesCsvParser
from src.application.usecases.create_countries.csv_parser import CountriesCsvParser
from src.application.usecases.create_regions.csv_parser import RegionsCsvParser
from src.application.usecases.tickets.pdf.strategies.default.config import (
    DefaultPdfTicketAdapterConfig,
)
from src.application.usecases.user.login import Login
from src.infrastructure.admin.config import AdminConfig
from src.infrastructure.clients.exchange_rates.exchange_rates_service import (
    ExchangeRateService,
    ExchangeRateServiceConfig,
)
from src.infrastructure.clients.ticket_parsers.amadeus.config import AmadeusAPIConfig
from src.infrastructure.clients.ticket_parsers.aviasales.config import (
    AviasalesAPIConfig,
)
from src.infrastructure.depends.decorator import inject_dependencies
from src.infrastructure.depends.repos_container import ReposContainer
from src.infrastructure.email_sender.config import EmailSenderConfig
from src.infrastructure.jwt.jwt_config import JwtConfig
from src.infrastructure.jwt.jwt_processor import JwtProcessor
from src.infrastructure.pdf_service.service import PdfService
from src.infrastructure.redis.config import RedisConfig
from src.infrastructure.repositories.user_repository import UserRepository
from src.infrastructure.security.password_hasher import PasswordHasher


async def get_httpx_session():
    async with httpx.AsyncClient() as session:
        yield session


@lru_cache
def get_jwt_config() -> JwtConfig:
    return JwtConfig()


def get_jwt_processor(config: JwtConfig = get_jwt_config()) -> JwtProcessor:
    return JwtProcessor(config)


@lru_cache
def get_password_hasher() -> PasswordHasher:
    return PasswordHasher()


@inject_dependencies
async def get_login_interactor(
    user_repository: Annotated[UserRepository, ReposContainer.user_repository],
    jwt_processor: Annotated[JwtProcessor, get_jwt_processor],
    password_hasher: Annotated[PasswordHasher, get_password_hasher],
) -> Login:
    return Login(user_repository, jwt_processor, password_hasher)


@lru_cache
def get_email_config() -> EmailSenderConfig:
    return EmailSenderConfig()


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


def get_cities_csv_parser() -> CitiesCsvParser:
    return CitiesCsvParser()


@lru_cache
def get_admin_config() -> AdminConfig:
    return AdminConfig()


@lru_cache
def get_aviasales_ticket_parser_config() -> AviasalesAPIConfig:
    return AviasalesAPIConfig()


@lru_cache
def get_amadeus_ticket_parser_config() -> AmadeusAPIConfig:
    return AmadeusAPIConfig()


@lru_cache
def get_default_pdf_ticket_adapter_config() -> DefaultPdfTicketAdapterConfig:
    return DefaultPdfTicketAdapterConfig()


def get_pdf_service() -> PdfService:
    return PdfService()


@lru_cache
def get_exchange_rate_service_config() -> ExchangeRateServiceConfig:
    return ExchangeRateServiceConfig()


@lru_cache
def get_redis_config() -> RedisConfig:
    return RedisConfig()


def get_redis(config: RedisConfig = get_redis_config()) -> Redis:
    return Redis(host=config.host, port=config.port, db=config.db, decode_responses=True)


@inject_dependencies
async def get_exchange_rate_service(
    session: Annotated[httpx.AsyncClient, get_httpx_session],
    config: ExchangeRateServiceConfig = get_exchange_rate_service_config(),
    redis: Redis = get_redis(),
) -> ExchangeRateService:
    return ExchangeRateService(session, config, redis)
