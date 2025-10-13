from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from redis import Redis  # type: ignore

from avia.application.builders.user_ticket import UserTicketFullInfoAssembler
from avia.application.queries.get_aircrafts_dict import GetAircraftsDict
from avia.application.queries.get_airlines_dict import GetAirlinesDict
from avia.application.queries.get_airports_dict import GetAirportsDict
from avia.application.services.currency_converter import CurrencyConverter
from avia.application.usecases.tickets.pdf.config import PdfGeneratorConfig
from avia.application.usecases.tickets.pdf.strategies.default.adapter import (
    DefaultPdfTicketAdapter,
    DefaultPdfTicketAdapterConfig,
)
from avia.application.usecases.tickets.pdf.strategies.default.generator import (
    DefaultPdfTicketGenerator,
)
from avia.infrastructure.clients.exchange_rates.exchange_rates_service import (
    ExchangeRateService,
    ExchangeRateServiceConfig,
)
from avia.infrastructure.clients.ticket_parsers.amadeus.adapter import (
    AmadeusTicketAdapter,
)
from avia.infrastructure.clients.ticket_parsers.amadeus.config import AmadeusAPIConfig
from avia.infrastructure.clients.ticket_parsers.amadeus.parser import (
    AmadeusTicketParser,
)
from avia.infrastructure.clients.ticket_parsers.aviasales.adapter import (
    AviasalesTicketAdapter,
)
from avia.infrastructure.clients.ticket_parsers.aviasales.config import (
    AviasalesAPIConfig,
)
from avia.infrastructure.clients.ticket_parsers.aviasales.parser import (
    AviasalesTicketParser,
)
from avia.infrastructure.depends.base import (
    get_amadeus_ticket_parser_config,
    get_aviasales_ticket_parser_config,
    get_default_pdf_ticket_adapter_config,
    get_email_config,
    get_pdf_service,
    get_redis_config,
)
from avia.infrastructure.email_sender.config import EmailSenderConfig
from avia.infrastructure.email_sender.service import EmailSender
from avia.infrastructure.jwt.jwt_config import JwtConfig
from avia.infrastructure.jwt.jwt_processor import JwtProcessor
from avia.infrastructure.pdf_service.service import PdfService
from avia.infrastructure.persistence.data_mappers.insurance_files_data_mapper import (
    InsuranceFilesDataMapper,
)
from avia.infrastructure.persistence.data_mappers.ticket_files_data_mapper import (
    TicketFilesDataMapper,
)
from avia.infrastructure.persistence.file_manager import FileManager
from avia.infrastructure.redis.config import RedisConfig
from avia.infrastructure.tg_notifier.config import TelegramSenderConfig
from avia.infrastructure.tg_notifier.notifier import TgNotifier
from avia.infrastructure.timezone_resolver import TimezoneResolver
from avia.web.depends.annotations.annotations import (
    AircraftRepositoryAnnotation,
    AirlineRepositoryAnnotation,
    AirportRepositoryAnnotation,
    TicketDAOAnnotation,
    UserRepositoryAnnotation,
)
from avia.web.depends.annotations.db_annotation import DbAnnotation
from avia.web.depends.annotations.httpx_session import HttpxSessionAnnotation


@lru_cache
def get_jwt_config() -> JwtConfig:
    return JwtConfig()


def get_jwt_processor(config: Annotated[JwtConfig, Depends(get_jwt_config)]) -> JwtProcessor:
    return JwtProcessor(config)


def get_file_manager() -> FileManager:
    return FileManager()


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


def get_redis(redis_config: Annotated[RedisConfig, Depends(get_redis_config)]) -> Redis:
    return Redis(
        host=redis_config.host,
        port=redis_config.port,
        db=redis_config.db,
        decode_responses=True,
    )


def get_timezone_resolver(redis: Annotated[Redis, Depends(get_redis)]) -> TimezoneResolver:
    return TimezoneResolver(redis=redis)


def get_airports_dict(repository: AirportRepositoryAnnotation) -> GetAirportsDict:
    return GetAirportsDict(repository)


def get_airlines_dict(repository: AirlineRepositoryAnnotation) -> GetAirlinesDict:
    return GetAirlinesDict(repository)


def get_aircrafts_dict(repository: AircraftRepositoryAnnotation) -> GetAircraftsDict:
    return GetAircraftsDict(repository)


@lru_cache
def get_tg_config() -> TelegramSenderConfig:
    return TelegramSenderConfig()


def get_tg_notifier(config: Annotated[TelegramSenderConfig, Depends(get_tg_config)]) -> TgNotifier:
    return TgNotifier(config=config)


def get_amadeus_ticket_adapter(
    airports_query: Annotated[GetAirportsDict, Depends(get_airports_dict)],
    airlines_query: Annotated[GetAirlinesDict, Depends(get_airlines_dict)],
    aircrafts_query: Annotated[GetAircraftsDict, Depends(get_aircrafts_dict)],
    error_notifier: Annotated[TgNotifier, Depends(get_tg_notifier)],
    timezone_resolver: Annotated[TimezoneResolver, Depends(get_timezone_resolver)],
) -> AmadeusTicketAdapter:
    return AmadeusTicketAdapter(
        airports_query=airports_query,
        airlines_query=airlines_query,
        timezone_resolver=timezone_resolver,
        aircrafts_query=aircrafts_query,
        error_notifier=error_notifier,
    )


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


@lru_cache
def get_pdf_generator_config() -> PdfGeneratorConfig:
    return PdfGeneratorConfig()


def get_ticket_files_data_mapper(db: DbAnnotation) -> TicketFilesDataMapper:
    return TicketFilesDataMapper(db)


def get_insurance_data_mapper(db: DbAnnotation) -> InsuranceFilesDataMapper:
    return InsuranceFilesDataMapper(db)
