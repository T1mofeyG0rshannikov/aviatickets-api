from typing import Annotated

from fastapi import Depends

from avia.application.builders.user_ticket import UserTicketFullInfoAssembler
from avia.application.factories.ticket.ticket_factory import TicketFactory
from avia.application.pdf_templates import PdfTemplatesEnum
from avia.application.persistence.bulk_savers.aircraft_saver import (
    AircraftBulkSaverInterface,
)
from avia.application.persistence.bulk_savers.airline_saver import (
    AirlineBulkSaverInterface,
)
from avia.application.persistence.bulk_savers.airport_saver import (
    AirportBulkSaverInterface,
)
from avia.application.persistence.bulk_savers.city_saver import CityBulkSaverInterface
from avia.application.persistence.bulk_savers.country_saver import (
    CountryBulkSaverInterface,
)
from avia.application.persistence.bulk_savers.region_saver import (
    RegionBulkSaverInterface,
)
from avia.application.persistence.data_mappers.insurance_files import (
    InsuranceFilesDataMapperInterface,
)
from avia.application.services.currency_converter import CurrencyConverter
from avia.application.services.file_manager import FileManagerInterface
from avia.application.services.pdf_service import PdfServiceInterface
from avia.application.usecases.aircraft.import_aircrafts.loader import AircraftsLoader
from avia.application.usecases.aircraft.import_aircrafts.usecase import ImportAircrafts
from avia.application.usecases.airline.import_airlines.usecase import ImportAirlines
from avia.application.usecases.airports.get.usecase import GetAirports
from avia.application.usecases.airports.import_airports.adapter import (
    AirportLoadDataToCreateDTOAdapter,
)
from avia.application.usecases.airports.import_airports.load_data_to_create_dto_adapter import (
    ConvertAirportLoadDataToCreateData,
)
from avia.application.usecases.airports.import_airports.usecase import ImportAirports
from avia.application.usecases.city.get import GetCities
from avia.application.usecases.city.import_cities.usecase import CreateCities
from avia.application.usecases.country.get import GetCountries
from avia.application.usecases.country.get_or_create_countries_by_iso import (
    GetOrCreateCountriesByISO,
)
from avia.application.usecases.country.import_countries.usecase import ImportCountries
from avia.application.usecases.create_user_ticket import CreateUserTicket
from avia.application.usecases.insurance.create import CreateInsurance
from avia.application.usecases.insurance.generate_pdf import (
    GeneratePdfInsuranse,
    PdfInsuranceAdapter,
)
from avia.application.usecases.insurance.get_pdf import GetPdfInsurance
from avia.application.usecases.region.get_or_create_regions_by_iso import (
    GetOrCreateRegionsByISO,
)
from avia.application.usecases.region.import_regions.usecase import ImportRegions
from avia.application.usecases.tickets.email import SendPdfTicketToEmail
from avia.application.usecases.tickets.filter import FilterTickets
from avia.application.usecases.tickets.get import GetTicket
from avia.application.usecases.tickets.parse import ParseAviaTickets
from avia.application.usecases.tickets.pdf.config import PdfGeneratorConfig
from avia.application.usecases.tickets.pdf.generate import GeneratePdfTicket
from avia.application.usecases.tickets.pdf.get import GetPdfTicket
from avia.application.usecases.tickets.pdf.strategies.default.generator import (
    DefaultPdfTicketGenerator,
)
from avia.application.usecases.user.auth.login import Login
from avia.application.usecases.user.auth.register import Register
from avia.application.usecases.user.create import CreateUser
from avia.infrastructure.clients.ticket_parsers.amadeus.parser import (
    AmadeusTicketParser,
)
from avia.infrastructure.depends.base import get_pdf_service
from avia.infrastructure.email_sender.service import EmailSender
from avia.infrastructure.etl_parsers.aircrafts_parser import AircraftCsvParser
from avia.infrastructure.etl_parsers.airlines_parser import AirlinesTXTParser
from avia.infrastructure.etl_parsers.airports_parser import AirportsCsvParser
from avia.infrastructure.etl_parsers.cities_parser import CitiesCsvParser
from avia.infrastructure.etl_parsers.countries_parser import CountriesCsvParser
from avia.infrastructure.etl_parsers.regions_parser.parser import RegionsCsvParser
from avia.infrastructure.persistence.data_mappers.ticket_files_data_mapper import (
    TicketFilesDataMapper,
)
from avia.infrastructure.persistence.file_manager import FileManager
from avia.infrastructure.security.password_hasher import PasswordHasher
from avia.web.depends.annotations.annotations import (
    AircraftRepositoryAnnotation,
    AirlineRepositoryAnnotation,
    AirportDAOAnnotation,
    AirportRepositoryAnnotation,
    CitiesDAOAnnotation,
    CountriesDAOAnnotation,
    InsuranceRepositoryAnnotation,
    LocationRepositoryAnnotation,
    TicketDAOAnnotation,
    TicketRepositoryAnnotation,
    UserRepositoryAnnotation,
    UserTicketRepositoryAnnotation,
)
from avia.web.depends.annotations.db_annotation import DbAnnotation
from avia.web.depends.annotations.jwt_processor import JwtProcessorAnnotation
from avia.web.depends.bulk_savers import (
    get_aircraft_bulk_saver,
    get_airline_importer,
    get_airport_importer,
    get_city_importer,
    get_country_importer,
    get_region_importer,
)
from avia.web.depends.depends import (  # get_aviasales_ticket_parser,
    get_amadeus_ticket_parser,
    get_currency_converter,
    get_default_pdf_generator,
    get_email_sender,
    get_file_manager,
    get_insurance_data_mapper,
    get_pdf_generator_config,
    get_ticket_files_data_mapper,
    get_user_ticket_assembler,
)
from avia.web.depends.etl_loaders import (
    get_cities_csv_parser,
    get_countries_csv_parser,
    get_csv_airports_parser,
    get_regions_csv_parser,
    get_txt_airlines_parser,
)
from avia.web.depends.files_from_request import get_csv_file


def get_airport_load_data_to_create_data_adapter() -> AirportLoadDataToCreateDTOAdapter:
    return AirportLoadDataToCreateDTOAdapter()


def get_or_create_countries(
    persist_countries: Annotated[CountryBulkSaverInterface, Depends(get_country_importer)],
    location_repository: LocationRepositoryAnnotation,
) -> GetOrCreateCountriesByISO:
    return GetOrCreateCountriesByISO(persist_countries, location_repository)


def get_or_create_regions(
    persist_regions: Annotated[RegionBulkSaverInterface, Depends(get_region_importer)],
    location_repository: LocationRepositoryAnnotation,
) -> GetOrCreateRegionsByISO:
    return GetOrCreateRegionsByISO(persist_regions, location_repository)


def get_convert_airport_load_data_to_create_data(
    location_repository: LocationRepositoryAnnotation,
    adapter: Annotated[AirportLoadDataToCreateDTOAdapter, Depends(get_airport_load_data_to_create_data_adapter)],
    get_or_create_countries: Annotated[GetOrCreateCountriesByISO, Depends(get_or_create_countries)],
    get_or_create_regions: Annotated[GetOrCreateRegionsByISO, Depends(get_or_create_regions)],
) -> ConvertAirportLoadDataToCreateData:
    return ConvertAirportLoadDataToCreateData(
        location_repository=location_repository,
        adapter=adapter,
        get_or_create_countries_by_iso=get_or_create_countries,
        get_or_create_regions_by_iso=get_or_create_regions,
    )


def get_create_airports_interactor(
    repository: AirportRepositoryAnnotation,
    saver: Annotated[AirportBulkSaverInterface, Depends(get_airport_importer)],
    csv_parser: Annotated[AirportsCsvParser, Depends(get_csv_airports_parser)],
    converter: Annotated[ConvertAirportLoadDataToCreateData, Depends(get_convert_airport_load_data_to_create_data)],
    transaction: DbAnnotation,
) -> ImportAirports:
    return ImportAirports(
        saver=saver, loader=csv_parser, repository=repository, transaction=transaction, converter=converter
    )


def get_create_airlines_interactor(
    transaction: DbAnnotation,
    repository: AirlineRepositoryAnnotation,
    txt_parser: Annotated[AirlinesTXTParser, Depends(get_txt_airlines_parser)],
    importer: Annotated[AirlineBulkSaverInterface, Depends(get_airline_importer)],
) -> ImportAirlines:
    return ImportAirlines(repository, importer, txt_parser, transaction=transaction)


def get_create_countries_interactor(
    transaction: DbAnnotation,
    csv_parser: Annotated[CountriesCsvParser, Depends(get_countries_csv_parser)],
    repository: LocationRepositoryAnnotation,
    countries_bulk_saver: Annotated[CountryBulkSaverInterface, Depends(get_country_importer)],
) -> ImportCountries:
    return ImportCountries(
        loader=csv_parser, repository=repository, country_bulk_saver=countries_bulk_saver, transaction=transaction
    )


def get_create_regions_interactor(
    transaction: DbAnnotation,
    csv_parser: Annotated[RegionsCsvParser, Depends(get_regions_csv_parser)],
    repository: LocationRepositoryAnnotation,
    importer: Annotated[RegionBulkSaverInterface, Depends(get_region_importer)],
) -> ImportRegions:
    return ImportRegions(loader=csv_parser, repository=repository, importer=importer, transaction=transaction)


def get_aircraft_loader(data: Annotated[list[list[str]], Depends(get_csv_file)]) -> AircraftCsvParser:
    return AircraftCsvParser(data=data)


def get_import_aircrafts_interactor(
    transaction: DbAnnotation,
    repository: AircraftRepositoryAnnotation,
    saver: Annotated[AircraftBulkSaverInterface, Depends(get_aircraft_bulk_saver)],
    loader: Annotated[AircraftsLoader, Depends(get_aircraft_loader)],
) -> ImportAircrafts:
    return ImportAircrafts(transaction=transaction, repository=repository, saver=saver, loader=loader)


def get_create_cities_interactor(
    transaction: DbAnnotation,
    csv_parser: Annotated[CitiesCsvParser, Depends(get_cities_csv_parser)],
    repository: LocationRepositoryAnnotation,
    importer: Annotated[CityBulkSaverInterface, Depends(get_city_importer)],
) -> CreateCities:
    return CreateCities(loader=csv_parser, repository=repository, importer=importer, transaction=transaction)


def get_ticket_factory(airport_repository: AirportRepositoryAnnotation) -> TicketFactory:
    return TicketFactory(airport_repository)


def get_parse_tickets_interactor(
    transaction: DbAnnotation,
    # aviasales_parser: Annotated[AviasalesTicketParser, Depends(get_aviasales_ticket_parser)],
    amadeus_parser: Annotated[AmadeusTicketParser, Depends(get_amadeus_ticket_parser)],
    airports_repository: AirportRepositoryAnnotation,
    ticket_repository: TicketRepositoryAnnotation,
    ticket_factory: Annotated[TicketFactory, Depends(get_ticket_factory)],
) -> ParseAviaTickets:
    return ParseAviaTickets(
        parsers=[amadeus_parser],
        airports_repository=airports_repository,
        ticket_repository=ticket_repository,
        ticket_factory=ticket_factory,
        transaction=transaction,
    )


def get_filter_tickets_interactor(
    ticket_repository: TicketDAOAnnotation,
    currency_converter: Annotated[CurrencyConverter, Depends(get_currency_converter)],
) -> FilterTickets:
    return FilterTickets(ticket_repository, currency_converter)


def get_ticket_interactor(ticket_repository: TicketDAOAnnotation) -> GetTicket:
    return GetTicket(ticket_repository)


def get_generate_pdf_ticket_interactor(
    builder: Annotated[UserTicketFullInfoAssembler, Depends(get_user_ticket_assembler)],
    default_pdf_generator: Annotated[DefaultPdfTicketGenerator, Depends(get_default_pdf_generator)],
) -> GeneratePdfTicket:
    return GeneratePdfTicket(builder, strategies={PdfTemplatesEnum.default: default_pdf_generator})


def get_pdf_ticket_interactor(
    transaction: DbAnnotation,
    generate_pdf: Annotated[GeneratePdfTicket, Depends(get_generate_pdf_ticket_interactor)],
    file_manager: Annotated[FileManager, Depends(get_file_manager)],
    ticket_files_data_mapper: Annotated[TicketFilesDataMapper, Depends(get_ticket_files_data_mapper)],
    user_ticket_repository: UserTicketRepositoryAnnotation,
    config: Annotated[PdfGeneratorConfig, Depends(get_pdf_generator_config)],
) -> GetPdfTicket:
    return GetPdfTicket(
        file_manager=file_manager,
        generate_pdf=generate_pdf,
        user_ticket_repository=user_ticket_repository,
        ticket_files_data_mapper=ticket_files_data_mapper,
        config=config,
        transaction=transaction,
    )


def get_send_pdf_ticket_to_email_interactor(
    user_ticket_repository: UserTicketRepositoryAnnotation,
    get_pdf_ticket: Annotated[GetPdfTicket, Depends(get_pdf_ticket_interactor)],
    email_sender: Annotated[EmailSender, Depends(get_email_sender)],
) -> SendPdfTicketToEmail:
    return SendPdfTicketToEmail(
        user_ticket_repository=user_ticket_repository, get_pdf_ticket=get_pdf_ticket, email_sender=email_sender
    )


def get_create_user_ticket_interactor(
    transaction: DbAnnotation, repository: UserTicketRepositoryAnnotation, ticket_repository: TicketRepositoryAnnotation
) -> CreateUserTicket:
    return CreateUserTicket(repository, ticket_repository, transaction=transaction)


def get_password_hasher() -> PasswordHasher:
    return PasswordHasher()


def get_create_user(
    transaction: DbAnnotation,
    user_repository: UserRepositoryAnnotation,
    password_hasher: Annotated[PasswordHasher, Depends(get_password_hasher)],
) -> CreateUser:
    return CreateUser(user_repository, password_hasher, transaction=transaction)


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


def get_countries_interactor(countries_dao: CountriesDAOAnnotation) -> GetCountries:
    return GetCountries(countries_dao)


def get_cities_interactor(cities_dao: CitiesDAOAnnotation) -> GetCities:
    return GetCities(cities_dao)


def get_insurance_adapter(
    currency_converter: Annotated[CurrencyConverter, Depends(get_currency_converter)],
    user_repository: UserRepositoryAnnotation,
) -> PdfInsuranceAdapter:
    return PdfInsuranceAdapter(currency_converter=currency_converter, user_repository=user_repository)


def get_generate_pdf_insurance(
    config: Annotated[PdfGeneratorConfig, Depends(get_pdf_generator_config)],
    adapter: Annotated[PdfInsuranceAdapter, Depends(get_insurance_adapter)],
    pdf_service: Annotated[PdfServiceInterface, Depends(get_pdf_service)],
) -> GeneratePdfInsuranse:
    return GeneratePdfInsuranse(config=config, adapter=adapter, pdf_service=pdf_service)


def get_pdf_insurance_interactor(
    transaction: DbAnnotation,
    file_manager: Annotated[FileManagerInterface, Depends(get_file_manager)],
    generate_pdf: Annotated[GeneratePdfInsuranse, Depends(get_generate_pdf_insurance)],
    ticket_files_data_mapper: Annotated[InsuranceFilesDataMapperInterface, Depends(get_insurance_data_mapper)],
    repository: InsuranceRepositoryAnnotation,
    config: Annotated[PdfGeneratorConfig, Depends(get_pdf_generator_config)],
) -> GetPdfInsurance:
    return GetPdfInsurance(
        transaction=transaction,
        file_manager=file_manager,
        generate_pdf=generate_pdf,
        ticket_files_data_mapper=ticket_files_data_mapper,
        repository=repository,
        config=config,
    )


def get_create_insurance_interactor(
    transaction: DbAnnotation,
    repository: InsuranceRepositoryAnnotation,
    user_ticket_repository: UserTicketRepositoryAnnotation,
    ticket_repository: TicketRepositoryAnnotation,
    location_repository: LocationRepositoryAnnotation,
) -> CreateInsurance:
    return CreateInsurance(
        transaction=transaction,
        repository=repository,
        user_ticket_repository=user_ticket_repository,
        ticket_repository=ticket_repository,
        location_repository=location_repository,
    )
