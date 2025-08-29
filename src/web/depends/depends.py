from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from redis import Redis  # type: ignore

from src.infrastructure.etl_parsers.regions_parser.adapter import RegionsLoaderAdapter
from src.infrastructure.timezone_resolver import TimezoneResolver
from src.application.builders.user_ticket import UserTicketFullInfoAssembler
from src.application.services.currency_converter import CurrencyConverter
from src.application.usecases.tickets.pdf.strategies.default.adapter import (
    DefaultPdfTicketAdapter,
    DefaultPdfTicketAdapterConfig,
)
from src.application.usecases.tickets.pdf.strategies.default.generator import (
    DefaultPdfTicketGenerator,
)
from src.infrastructure.clients.exchange_rates.exchange_rates_service import (
    ExchangeRateService,
    ExchangeRateServiceConfig,
)
from src.infrastructure.clients.ticket_parsers.amadeus.adapter import (
    AmadeusTicketAdapter,
)
from src.infrastructure.clients.ticket_parsers.amadeus.config import AmadeusAPIConfig
from src.infrastructure.clients.ticket_parsers.amadeus.parser import AmadeusTicketParser
from src.infrastructure.clients.ticket_parsers.aviasales.adapter import (
    AviasalesTicketAdapter,
)
from src.infrastructure.clients.ticket_parsers.aviasales.config import (
    AviasalesAPIConfig,
)
from src.infrastructure.clients.ticket_parsers.aviasales.parser import (
    AviasalesTicketParser,
)
from src.infrastructure.depends.base import (
    get_amadeus_ticket_parser_config,
    get_aviasales_ticket_parser_config,
    get_default_pdf_ticket_adapter_config,
    get_email_config,
    get_pdf_service,
    get_redis_config,
)
from src.infrastructure.email_sender.config import EmailSenderConfig
from src.infrastructure.email_sender.service import EmailSender
from src.infrastructure.jwt.jwt_config import JwtConfig
from src.infrastructure.jwt.jwt_processor import JwtProcessor
from src.infrastructure.pdf_service.service import PdfService
from src.infrastructure.redis.config import RedisConfig
from src.web.depends.annotations.annotations import (
    AirlineRepositoryAnnotation,
    AirportRepositoryAnnotation,
    LocationRepositoryAnnotation,
    TicketDAOAnnotation,
    UserRepositoryAnnotation,
)
from src.web.depends.annotations.httpx_session import HttpxSessionAnnotation


@lru_cache
def get_jwt_config() -> JwtConfig:
    return JwtConfig()


def get_jwt_processor(config: Annotated[JwtConfig, Depends(get_jwt_config)]) -> JwtProcessor:
    return JwtProcessor(config)


def get_aviasales_ticket_adapter(
    repository: AirportRepositoryAnnotation,
    airline_repository: AirlineRepositoryAnnotation,
) -> AviasalesTicketAdapter:
    return AviasalesTicketAdapter(repository, airline_repository)


def get_aviasales_ticket_parser(
    session: HttpxSessionAnnotation,
    config: Annotated[AviasalesAPIConfig, Depends(get_aviasales_ticket_parser_config)],
    repository: AirportRepositoryAnnotation,
    adapter: Annotated[AviasalesTicketAdapter, Depends(get_aviasales_ticket_adapter)],
) -> AviasalesTicketParser:
    return AviasalesTicketParser(session, config, repository, adapter)


def get_timezone_resolver() -> TimezoneResolver:
    return TimezoneResolver()


def get_amadeus_ticket_adapter(
    repository: AirportRepositoryAnnotation,
    airline_repository: AirlineRepositoryAnnotation,
    timezone_resolver: Annotated[TimezoneResolver, Depends(get_timezone_resolver)],
) -> AmadeusTicketAdapter:
    return AmadeusTicketAdapter(repository, airline_repository, timezone_resolver)


def get_amadeus_ticket_parser(
    session: HttpxSessionAnnotation,
    repository: AirportRepositoryAnnotation,
    config: Annotated[AmadeusAPIConfig, Depends(get_amadeus_ticket_parser_config)],
    adapter: Annotated[AmadeusTicketAdapter, Depends(get_amadeus_ticket_adapter)],
) -> AmadeusTicketParser:
    return AmadeusTicketParser(session, config, repository, adapter)


def get_user_ticket_assembler(
    user_repository: UserRepositoryAnnotation,
    ticket_repository: TicketDAOAnnotation,
) -> UserTicketFullInfoAssembler:
    return UserTicketFullInfoAssembler(user_repository, ticket_repository)


def get_email_sender(config: Annotated[EmailSenderConfig, Depends(get_email_config)]) -> EmailSender:
    return EmailSender(config)


@lru_cache
def get_exchange_rate_service_config() -> ExchangeRateServiceConfig:
    return ExchangeRateServiceConfig()


def get_redis(config: Annotated[RedisConfig, Depends(get_redis_config)]) -> Redis:
    return Redis(host=config.host, port=config.port, db=config.db, decode_responses=True)


def get_exchange_rate_service(
    session: HttpxSessionAnnotation,
    config: Annotated[ExchangeRateServiceConfig, Depends(get_exchange_rate_service_config)],
    redis: Annotated[Redis, Depends(get_redis)],
) -> ExchangeRateService:
    return ExchangeRateService(session, config, redis)


def get_currency_converter(
    exchange_rate_service: Annotated[ExchangeRateService, Depends(get_exchange_rate_service)]
) -> CurrencyConverter:
    return CurrencyConverter(exchange_rate_service)


def get_default_pdf_ticket_adapter(
    config: Annotated[DefaultPdfTicketAdapterConfig, Depends(get_default_pdf_ticket_adapter_config)],
    currency_converter: Annotated[CurrencyConverter, Depends(get_currency_converter)],
) -> DefaultPdfTicketAdapter:
    return DefaultPdfTicketAdapter(config, currency_converter)


def get_default_pdf_generator(
    adapter: Annotated[DefaultPdfTicketAdapter, Depends(get_default_pdf_ticket_adapter)],
    pdf_service: Annotated[PdfService, Depends(get_pdf_service)],
) -> DefaultPdfTicketGenerator:
    return DefaultPdfTicketGenerator(adapter, pdf_service)
