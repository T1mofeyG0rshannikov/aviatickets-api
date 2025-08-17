from typing import Annotated

from fastapi import Depends

from src.depends.annotations.annotations import (
    AirlineRepositoryAnnotation,
    AirportRepositoryAnnotation,
    LocationRepositoryAnnotation,
    TicketReadRepositoryAnnotation,
    TicketRepositoryAnnotation,
    UserRepositoryAnnotation,
    UserTicketRepositoryAnnotation,
)
from src.depends.annotations.jwt_processor import JwtProcessorAnnotation
from src.depends.depends import (
    get_airports_scv_to_dto_adapter,
    get_aviasales_ticket_parser,
    get_cities_csv_parser,
    get_countries_csv_parser,
    get_csv_airports_parser,
    get_email_sender,
    get_password_hasher,
    get_pdf_service,
    get_pdf_ticket_adapter,
    get_regions_csv_parser,
    get_regions_csv_to_create_adapter,
    get_txt_airlines_parser,
    get_user_ticket_assembler,
)
from src.infrastructure.email_sender.service import EmailSender
from src.infrastructure.pdf_service.service import PdfService
from src.infrastructure.security.password_hasher import PasswordHasher
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
from src.usecases.create_user_ticket.usecase import CreateUserTicket
from src.usecases.tickets.email.usecase import SendPdfTicketToEmail
from src.usecases.tickets.filter.usecase import FilterTickets
from src.usecases.tickets.parse.parsers.aviasales.parser import AviasalesTicketParser
from src.usecases.tickets.parse.usecase import ParseAviaTickets
from src.usecases.tickets.pdf.adapter import PdfTicketAdapter
from src.usecases.tickets.pdf.usecase import (
    CreatePdfTicket,
    UserTicketFullInfoAssembler,
)
from src.usecases.user.login import Login
from src.usecases.user.register import Register


def get_create_airports_interactor(
    repository: AirportRepositoryAnnotation,
    csv_parser: Annotated[AirportsCsvParser, Depends(get_csv_airports_parser)],
    adapter: Annotated[AirportsCsvToCreateDTOAdapter, Depends(get_airports_scv_to_dto_adapter)],
    location_repository: LocationRepositoryAnnotation,
) -> CreateAirports:
    return CreateAirports(repository, csv_parser, adapter, location_repository)


def get_create_airlines_interactor(
    repository: AirlineRepositoryAnnotation, txt_parser: Annotated[AirlinesTXTParser, Depends(get_txt_airlines_parser)]
) -> CreateAirlines:
    return CreateAirlines(repository, txt_parser)


def get_create_countries_interactor(
    csv_parser: Annotated[CountriesCsvParser, Depends(get_countries_csv_parser)],
    repository: LocationRepositoryAnnotation,
) -> CreateCountries:
    return CreateCountries(csv_parser, repository)


def get_create_regions_interactor(
    csv_parser: Annotated[RegionsCsvParser, Depends(get_regions_csv_parser)],
    repository: LocationRepositoryAnnotation,
    adapter: Annotated[RegionCsvToCreateDTOAdapter, Depends(get_regions_csv_to_create_adapter)],
) -> CreateRegions:
    return CreateRegions(csv_parser=csv_parser, repository=repository, adapter=adapter)


def get_create_cities_interactor(
    csv_parser: Annotated[CitiesCsvParser, Depends(get_cities_csv_parser)],
    repository: LocationRepositoryAnnotation,
) -> CreateCities:
    return CreateCities(
        csv_parser=csv_parser,
        repository=repository,
    )


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


def get_create_pdf_ticket_interactor(
    adapter: Annotated[PdfTicketAdapter, Depends(get_pdf_ticket_adapter)],
    user_ticket_repository: UserTicketRepositoryAnnotation,
    builder: Annotated[UserTicketFullInfoAssembler, Depends(get_user_ticket_assembler)],
    pdf_service: Annotated[PdfService, Depends(get_pdf_service)],
) -> CreatePdfTicket:
    return CreatePdfTicket(adapter, user_ticket_repository, builder, pdf_service)


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


def get_register_interactor(
    user_repository: UserRepositoryAnnotation,
    jwt_processor: JwtProcessorAnnotation,
    password_hasher: Annotated[PasswordHasher, Depends(get_password_hasher)],
) -> Register:
    return Register(user_repository, jwt_processor, password_hasher)


def get_login_interactor(
    user_repository: UserRepositoryAnnotation,
    jwt_processor: JwtProcessorAnnotation,
    password_hasher: Annotated[PasswordHasher, Depends(get_password_hasher)],
) -> Login:
    return Login(user_repository, jwt_processor, password_hasher)
