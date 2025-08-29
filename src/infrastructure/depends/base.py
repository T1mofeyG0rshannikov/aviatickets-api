from functools import lru_cache

import httpx
from dependency_injector import containers, providers
from redis import Redis

from src.infrastructure.etl_parsers.airports_parser.adapter import CsvToAirportAdapter
from src.infrastructure.etl_parsers.airports_parser.airports_parser import AirportsCsvParser
from src.infrastructure.etl_parsers.airlines_parser import AirlinesTXTParser
from src.infrastructure.etl_parsers.regions_parser.parser import RegionsCsvParser
from src.application.usecases.tickets.pdf.strategies.default.config import (
    DefaultPdfTicketAdapterConfig,
)
from src.application.usecases.user.auth.login import Login
from src.infrastructure.admin.auth import AdminAuth
from src.infrastructure.admin.config import AdminConfig
from src.infrastructure.clients.exchange_rates.exchange_rates_service import (
    ExchangeRateService,
    ExchangeRateServiceConfig,
)
from src.infrastructure.clients.ticket_parsers.amadeus.config import AmadeusAPIConfig
from src.infrastructure.clients.ticket_parsers.aviasales.config import (
    AviasalesAPIConfig,
)
from src.infrastructure.depends.repos_container import ReposContainer
from src.infrastructure.email_sender.config import EmailSenderConfig
from src.infrastructure.factories.login import LoginFactory
from src.infrastructure.jwt.jwt_config import JwtConfig
from src.infrastructure.jwt.jwt_processor import JwtProcessor
from src.infrastructure.pdf_service.service import PdfService
from src.infrastructure.redis.config import RedisConfig
from src.infrastructure.security.password_hasher import PasswordHasher


async def get_httpx_session():
    async with httpx.AsyncClient() as session:
        yield session


class InfraDIContainer(containers.DeclarativeContainer):
    jwt_config = providers.Singleton(JwtConfig)
    jwt_processor = providers.Singleton(JwtProcessor, jwt_config)
    password_hasher = providers.Singleton(PasswordHasher)

    redis_config = providers.Singleton(RedisConfig)

    redis = providers.Singleton(
        Redis,
        host=redis_config.provided.host,
        port=redis_config.provided.port,
        db=redis_config.provided.db,
        decode_responses=True,
    )

    session = providers.Resource(get_httpx_session)
    exchange_rate_service_config = providers.Singleton(ExchangeRateServiceConfig)

    exchange_rate_service = providers.Factory(
        ExchangeRateService, session=session, config=exchange_rate_service_config, redis=redis
    )

    admin_config = providers.Singleton(AdminConfig)

    admin_auth = providers.Singleton(
        AdminAuth,
        jwt_processor=jwt_processor,
        password_hasher=password_hasher,
        config=admin_config,
        login_factory=LoginFactory,
    )


@lru_cache
def get_email_config() -> EmailSenderConfig:
    return EmailSenderConfig()


def get_csv_to_airport_adapter() -> CsvToAirportAdapter:
    return CsvToAirportAdapter()


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


# infra_di_container = InfraDIContainer()
# infra_di_container.wire(modules=["src.infrastructure"])
