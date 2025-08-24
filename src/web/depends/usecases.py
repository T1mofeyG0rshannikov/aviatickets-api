from typing import Annotated

from fastapi import Depends

from src.application.builders.user_ticket import UserTicketFullInfoAssembler
from src.application.etl_importers.airline_importer import AirlineImporterInterface
from src.application.etl_importers.airport_importer import AirportImporterInterface
from src.application.etl_importers.city_importer import CityImporterInterface
from src.application.etl_importers.country_importer import CountryImporterInterface
from src.application.etl_importers.region_importer import RegionImporterInterface
from src.application.services.currency_converter import CurrencyConverter
from src.application.usecases.airports.create.adapter import CsvToAirportAdapter
from src.application.usecases.airports.create.csv_parser import AirportsCsvParser
from src.application.usecases.airports.create.usecase import CreateAirports
from src.application.usecases.airports.get.usecase import GetAirports
from src.application.usecases.create_airlines.txt_parser import AirlinesTXTParser
from src.application.usecases.create_airlines.usecase import CreateAirlines
from src.application.usecases.create_cities.csv_parser import CitiesCsvParser
from src.application.usecases.create_cities.usecase import CreateCities
from src.application.usecases.create_countries.csv_parser import CountriesCsvParser
from src.application.usecases.create_countries.usecase import CreateCountries
from src.application.usecases.create_regions.adapter import RegionCsvToEntitiesAdapter
from src.application.usecases.create_regions.csv_parser import RegionsCsvParser
from src.application.usecases.create_regions.usecase import CreateRegions
from src.application.usecases.create_user_ticket import CreateUserTicket
from src.application.usecases.tickets.email import SendPdfTicketToEmail
from src.application.usecases.tickets.filter import FilterTickets
from src.application.usecases.tickets.get import GetTicket
from src.application.usecases.tickets.parse import ParseAviaTickets
from src.application.usecases.tickets.pdf.strategies.default.generator import (
    DefaultPdfTicketGenerator,
)
from src.application.usecases.tickets.pdf.usecase import CreatePdfTicket
from src.application.usecases.user.auth.login import Login
from src.application.usecases.user.auth.register import Register
from src.application.usecases.user.create import CreateUser
from src.infrastructure.clients.ticket_parsers.amadeus.parser import AmadeusTicketParser
from src.infrastructure.clients.ticket_parsers.aviasales.parser import (
    AviasalesTicketParser,
)
from src.infrastructure.depends.base import (
    get_cities_csv_parser,
    get_countries_csv_parser,
    get_csv_airports_parser,
    get_csv_to_airport_adapter,
    get_regions_csv_parser,
    get_txt_airlines_parser,
)
from src.infrastructure.email_sender.service import EmailSender
from src.infrastructure.security.password_hasher import PasswordHasher
from src.interface_adapters.pdf_templates import PdfTemplatesEnum
from src.web.depends.annotations.annotations import (
    AirlineRepositoryAnnotation,
    AirportDAOAnnotation,
    AirportRepositoryAnnotation,
    LocationRepositoryAnnotation,
    TicketDAOAnnotation,
    TicketRepositoryAnnotation,
    UserRepositoryAnnotation,
    UserTicketRepositoryAnnotation,
)
from src.web.depends.annotations.jwt_processor import JwtProcessorAnnotation
from src.web.depends.depends import (
    get_amadeus_ticket_parser,
    get_aviasales_ticket_parser,
    get_currency_converter,
    get_default_pdf_generator,
    get_email_sender,
    get_regions_csv_to_create_adapter,
    get_user_ticket_assembler,
)
from src.web.depends.importers import (
    get_airline_importer,
    get_airport_importer,
    get_city_importer,
    get_country_importer,
    get_region_importer,
)


def get_create_airports_interactor(
    repository: AirportRepositoryAnnotation,
    importer: Annotated[AirportImporterInterface, Depends(get_airport_importer)],
    csv_parser: Annotated[AirportsCsvParser, Depends(get_csv_airports_parser)],
    adapter: Annotated[CsvToAirportAdapter, Depends(get_csv_to_airport_adapter)],
    location_repository: LocationRepositoryAnnotation,
) -> CreateAirports:
    return CreateAirports(repository, importer, csv_parser, adapter, location_repository)


def get_create_airlines_interactor(
    repository: AirlineRepositoryAnnotation,
    txt_parser: Annotated[AirlinesTXTParser, Depends(get_txt_airlines_parser)],
    importer: Annotated[AirlineImporterInterface, Depends(get_airline_importer)],
) -> CreateAirlines:
    return CreateAirlines(repository, importer, txt_parser)


def get_create_countries_interactor(
    csv_parser: Annotated[CountriesCsvParser, Depends(get_countries_csv_parser)],
    repository: LocationRepositoryAnnotation,
    importer: Annotated[CountryImporterInterface, Depends(get_country_importer)],
) -> CreateCountries:
    return CreateCountries(csv_parser, repository, importer)


def get_create_regions_interactor(
    csv_parser: Annotated[RegionsCsvParser, Depends(get_regions_csv_parser)],
    repository: LocationRepositoryAnnotation,
    importer: Annotated[RegionImporterInterface, Depends(get_region_importer)],
    adapter: Annotated[RegionCsvToEntitiesAdapter, Depends(get_regions_csv_to_create_adapter)],
) -> CreateRegions:
    return CreateRegions(csv_parser=csv_parser, repository=repository, importer=importer, adapter=adapter)


def get_create_cities_interactor(
    csv_parser: Annotated[CitiesCsvParser, Depends(get_cities_csv_parser)],
    repository: LocationRepositoryAnnotation,
    importer: Annotated[CityImporterInterface, Depends(get_city_importer)],
) -> CreateCities:
    return CreateCities(csv_parser=csv_parser, repository=repository, importer=importer)


def get_parse_tickets_interactor(
    aviasales_parser: Annotated[AviasalesTicketParser, Depends(get_aviasales_ticket_parser)],
    amadeus_parser: Annotated[AmadeusTicketParser, Depends(get_amadeus_ticket_parser)],
    airports_repository: AirportRepositoryAnnotation,
    ticket_repository: TicketRepositoryAnnotation,
) -> ParseAviaTickets:
    return ParseAviaTickets(
        parsers=[aviasales_parser, amadeus_parser],
        airports_repository=airports_repository,
        ticket_repository=ticket_repository,
    )


def get_filter_tickets_interactor(
    ticket_repository: TicketDAOAnnotation,
    currency_converter: Annotated[CurrencyConverter, Depends(get_currency_converter)],
) -> FilterTickets:
    return FilterTickets(ticket_repository, currency_converter)


def get_ticket_interactor(ticket_repository: TicketDAOAnnotation) -> GetTicket:
    return GetTicket(ticket_repository)


def get_create_pdf_ticket_interactor(
    user_ticket_repository: UserTicketRepositoryAnnotation,
    builder: Annotated[UserTicketFullInfoAssembler, Depends(get_user_ticket_assembler)],
    default_pdf_generator: Annotated[DefaultPdfTicketGenerator, Depends(get_default_pdf_generator)],
) -> CreatePdfTicket:
    return CreatePdfTicket(
        user_ticket_repository, builder, strategies={PdfTemplatesEnum.default: default_pdf_generator}
    )


def get_send_pdf_ticket_to_email_interactor(
    user_ticket_repository: UserTicketRepositoryAnnotation,
    create_pdf_ticket: Annotated[CreatePdfTicket, Depends(get_create_pdf_ticket_interactor)],
    email_sender: Annotated[EmailSender, Depends(get_email_sender)],
) -> SendPdfTicketToEmail:
    return SendPdfTicketToEmail(user_ticket_repository, create_pdf_ticket, email_sender)


def get_create_user_ticket_interactor(
    repository: UserTicketRepositoryAnnotation, ticket_repository: TicketRepositoryAnnotation
) -> CreateUserTicket:
    return CreateUserTicket(repository, ticket_repository)


def get_password_hasher() -> PasswordHasher:
    return PasswordHasher()


def get_create_user(
    user_repository: UserRepositoryAnnotation,
    password_hasher: Annotated[PasswordHasher, Depends(get_password_hasher)],
) -> CreateUser:
    return CreateUser(user_repository, password_hasher)


def get_register_interactor(
    create_user: Annotated[CreateUser, Depends(get_create_user)],
    jwt_processor: JwtProcessorAnnotation,
) -> Register:
    return Register(create_user, jwt_processor)


def get_login_interactor(
    user_repository: UserRepositoryAnnotation,
    jwt_processor: JwtProcessorAnnotation,
    password_hasher: Annotated[PasswordHasher, Depends(get_password_hasher)],
) -> Login:
    return Login(user_repository, jwt_processor, password_hasher)


def get_airports_interactor(airport_read_repository: AirportDAOAnnotation) -> GetAirports:
    return GetAirports(airport_read_repository)
