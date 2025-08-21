import datetime
from unittest.mock import MagicMock

import pytest

from src.application.builders.user_ticket import UserTicketFullInfoAssembler
from src.application.dto.airports.full_info import AirportFullInfoDTO
from src.application.dto.ticket import TicketFullInfoDTO, TicketSegmentFullInfoDTO
from src.application.dto.user_ticket import AdapterPdfField, UserTicketFullInfoDTO
from src.application.services.currency_converter import CurrencyConverter
from src.application.usecases.create_user_ticket import CreateUserTicket
from src.application.usecases.tickets.pdf.strategies.default.adapter import (
    DefaultPdfTicketAdapter,
    PdfFieldsAdapter,
)
from src.application.usecases.tickets.pdf.strategies.default.config import (
    DefaultPdfTicketAdapterConfig,
)
from src.application.usecases.tickets.pdf.strategies.default.generator import (
    DefaultPdfTicketGenerator,
)
from src.application.usecases.tickets.pdf.usecase import CreatePdfTicket
from src.entities.airline.airline import Airline
from src.entities.city.city import City
from src.entities.country.country import Country
from src.entities.exceptions import AccessDeniedError
from src.entities.region.region import Region
from src.entities.user.user import User
from src.entities.user_ticket.dto import CreatePassengerDTO
from src.entities.user_ticket.user_ticket import Passenger, UserTicket
from src.infrastructure.depends.base import get_default_pdf_ticket_adapter_config
from src.infrastructure.pdf_service.service import PdfService
from src.infrastructure.repositories.tickets_read_repository import TicketReadRepository
from src.infrastructure.repositories.user_repository import UserRepository
from src.infrastructure.repositories.user_ticket_repository import UserTicketRepository
from src.interface_adapters.file import File
from src.interface_adapters.pdf_templates import PdfTemplatesEnum


@pytest.fixture
def pdf_service() -> PdfService:
    return PdfService()


@pytest.fixture
async def user_ticket_assembler(
    user_repository: UserRepository,
    ticket_read_repository: TicketReadRepository,
    user_ticket_repository: UserTicketRepository,
) -> UserTicketFullInfoAssembler:
    return UserTicketFullInfoAssembler(user_repository, ticket_read_repository, user_ticket_repository)


@pytest.fixture
def config() -> DefaultPdfTicketAdapterConfig:
    return DefaultPdfTicketAdapterConfig()


@pytest.fixture
async def pdf_ticket_adapter(
    currency_converter: CurrencyConverter,
    config: DefaultPdfTicketAdapterConfig = get_default_pdf_ticket_adapter_config(),
) -> DefaultPdfTicketAdapter:
    return DefaultPdfTicketAdapter(config, currency_converter)


@pytest.fixture
async def mock_user_ticket_repository(db):
    return UserTicketRepository(db)


@pytest.fixture
def default_pdf_generator(
    pdf_ticket_adapter: DefaultPdfTicketAdapter,
    pdf_service: PdfService,
) -> DefaultPdfTicketGenerator:
    return DefaultPdfTicketGenerator(pdf_ticket_adapter, pdf_service)


@pytest.fixture
async def create_pdf_ticket(
    default_pdf_generator: DefaultPdfTicketGenerator,
    user_ticket_repository: UserTicketRepository,
    user_ticket_assembler: UserTicketFullInfoAssembler,
) -> CreatePdfTicket:
    return CreatePdfTicket(
        user_ticket_repository, user_ticket_assembler, strategies={PdfTemplatesEnum.default: default_pdf_generator}
    )


@pytest.mark.asyncio
async def test_create_pdf(
    create_pdf_ticket: CreatePdfTicket, user_repository: UserRepository, create_user_ticket: CreateUserTicket
):
    user = await user_repository.get(id=2)

    await create_user_ticket(
        ticket_id=194,
        passangers=[
            CreatePassengerDTO(
                first_name="Тимофей",
                second_name="Марков",
                gender="Мужской",
                birth_date=datetime.datetime(year=2025, month=1, day=1),
                passport="111111111",
                expiration_date=datetime.datetime(year=2027, month=1, day=1),
            )
        ],
        user=user,
    )

    result = await create_pdf_ticket(user_ticket_id=1, user=user)

    assert isinstance(result, File)


@pytest.mark.asyncio
async def test_assecc_denied_create_pdf_ticket(create_pdf_ticket: CreatePdfTicket, user_repository: UserRepository):
    user = await user_repository.get(id=3)
    user_ticket_mock = MagicMock(spec=UserTicket)
    user_ticket_mock.user_id = 2

    create_pdf_ticket.user_ticket_repository = MagicMock(spec=UserTicketRepository)
    create_pdf_ticket.user_ticket_repository.get.return_value = user_ticket_mock

    with pytest.raises(AccessDeniedError) as excinfo:
        await create_pdf_ticket(user_ticket_id=1, user=user)

    assert "Вы можете генерировать только свои билеты в pdf" in str(excinfo.value)


@pytest.mark.asyncio
async def test_default_pdf_template_adapter(pdf_ticket_adapter: DefaultPdfTicketAdapter):
    expected_result = [
        PdfFieldsAdapter(
            template_name="C:/Users/tgors/Desktop/top.pdf",
            data_fields_list=[
                [
                    AdapterPdfField(name="reservationCode", value="Not Available"),
                    AdapterPdfField(name="originDateShort", value="21-08-2025"),
                    AdapterPdfField(name="destinationDateShort", value="21-08-2025"),
                    AdapterPdfField(name="fromTo", value="MOSCOW, RUSSIA - DUBAI, UAE"),
                    AdapterPdfField(name="currency", value="RUB"),
                    AdapterPdfField(name="price", value="122,680.10"),
                    AdapterPdfField(name="passengers", value="STRING/STRING\n"),
                ]
            ],
        ),
        PdfFieldsAdapter(
            template_name="C:/Users/tgors/Desktop/new-single-ticket.pdf",
            data_fields_list=[
                [
                    AdapterPdfField(name="originFlight", value="AT-221"),
                    AdapterPdfField(name="originDepartingTime", value="02:30"),
                    AdapterPdfField(name="originDepartingDate", value="21 AUGUST 2025"),
                    AdapterPdfField(name="originArrivingDate", value="21 Aug 2025"),
                    AdapterPdfField(name="originArrivingTime", value="09:45"),
                    AdapterPdfField(name="Text-AUYa372fuH", value="THURSDAY 21 AUGUST 2025"),
                    AdapterPdfField(name="originDate", value="THURSDAY 21 AUGUST 2025"),
                    AdapterPdfField(name="originAirline", value="Royal Air Maroc"),
                    AdapterPdfField(name="originStatus", value="confirmed"),
                    AdapterPdfField(name="originClass", value="economy"),
                    AdapterPdfField(name="originAirportAddress", value="MOSCOW, RUSSIA"),
                    AdapterPdfField(name="originAirport", value="SVO"),
                    AdapterPdfField(name="destinationAirport", value="CMN"),
                    AdapterPdfField(name="destinationAirportAddress", value="CASABLANCA, MOROCCO"),
                    AdapterPdfField(name="passengers", value="STRING/STRING\n"),
                ],
                [
                    AdapterPdfField(name="originFlight", value="AT-9900"),
                    AdapterPdfField(name="originDepartingTime", value="09:45"),
                    AdapterPdfField(name="originDepartingDate", value="21 AUGUST 2025"),
                    AdapterPdfField(name="originArrivingDate", value="21 Aug 2025"),
                    AdapterPdfField(name="originArrivingTime", value="17:15"),
                    AdapterPdfField(name="Text-AUYa372fuH", value="THURSDAY 21 AUGUST 2025"),
                    AdapterPdfField(name="originDate", value="THURSDAY 21 AUGUST 2025"),
                    AdapterPdfField(name="originAirline", value="Royal Air Maroc"),
                    AdapterPdfField(name="originStatus", value="confirmed"),
                    AdapterPdfField(name="originClass", value="economy"),
                    AdapterPdfField(name="originAirportAddress", value="CASABLANCA, MOROCCO"),
                    AdapterPdfField(name="originAirport", value="CMN"),
                    AdapterPdfField(name="destinationAirport", value="DXB"),
                    AdapterPdfField(name="destinationAirportAddress", value="DUBAI, UAE"),
                    AdapterPdfField(name="passengers", value="STRING/STRING\n"),
                ],
            ],
        ),
        PdfFieldsAdapter(template_name="C:/Users/tgors/Desktop/bottom.pdf", data_fields_list=[]),
    ]

    mock_user_ticket = UserTicketFullInfoDTO(
        id=12,
        user=User(
            id=2,
            first_name="Тимофей",
            second_name="Марков",
            email="tgorshannikov@mail.ru",
            hash_password="$2b$12$sGj8.ZB2v5kRkXhjZLqcZu3j2u9gAddSF0gcqdipct8Qdydz/I9Va",
            is_superuser=True,
            is_active=True,
        ),
        ticket=TicketFullInfoDTO(
            id=225,
            duration=1065,
            price=1312.38,
            currency="EUR",
            transfers=2,
            segments=[
                TicketSegmentFullInfoDTO(
                    id=201,
                    flight_number="221",
                    destination_airport=AirportFullInfoDTO(
                        id=29683,
                        name="Mohammed V International Airport",
                        continent="AF",
                        country=Country(id=150, iso="MA", name="Марокко", name_english="Morocco"),
                        region=None,
                        city=City(id=615, name="Касабланка", name_english="Casablanca"),
                        scheduled_service="yes",
                        icao="GMMN",
                        iata="CMN",
                        gps_code="GMMN",
                        name_russian="Casabianca",
                    ),
                    origin_airport=AirportFullInfoDTO(
                        id=78233,
                        name="Sheremetyevo International Airport",
                        continent="EU",
                        country=Country(id=183, iso="RU", name="Россия", name_english="Russia"),
                        region=Region(
                            id=111, iso="RU-MOS", name="Московская область", name_english="Moskovskaya oblast"
                        ),
                        city=City(id=2342, name="Москва", name_english="Moscow"),
                        scheduled_service="yes",
                        icao="UUEE",
                        iata="SVO",
                        gps_code="UUEE",
                        name_russian="Международный аэропорт Шереметьево",
                    ),
                    airline=Airline(
                        id=20, iata="AT", icao="RAM", name="Royal Air Maroc", name_russian="Royal Air Maroc"
                    ),
                    departure_at=datetime.datetime(2025, 8, 21, 2, 30, tzinfo=datetime.timezone.utc),
                    return_at=datetime.datetime(2025, 8, 21, 6, 45, tzinfo=datetime.timezone.utc),
                    duration=435,
                    status="confirmed",
                    seat_class="economy",
                ),
                TicketSegmentFullInfoDTO(
                    id=202,
                    flight_number="9900",
                    destination_airport=AirportFullInfoDTO(
                        id=51072,
                        name="Dubai International Airport",
                        continent="AS",
                        country=Country(id=233, iso="AE", name="Объединенные Арабские Эмираты", name_english="UAE"),
                        region=None,
                        city=City(id=930, name="Дубай", name_english="Dubai"),
                        scheduled_service="yes",
                        icao="OMDB",
                        iata="DXB",
                        gps_code="OMDB",
                        name_russian=None,
                    ),
                    origin_airport=AirportFullInfoDTO(
                        id=29683,
                        name="Mohammed V International Airport",
                        continent="AF",
                        country=Country(id=150, iso="MA", name="Марокко", name_english="Morocco"),
                        region=None,
                        city=City(id=615, name="Касабланка", name_english="Casablanca"),
                        scheduled_service="yes",
                        icao="GMMN",
                        iata="CMN",
                        gps_code="GMMN",
                        name_russian="Casabianca",
                    ),
                    airline=Airline(
                        id=20, iata="AT", icao="RAM", name="Royal Air Maroc", name_russian="Royal Air Maroc"
                    ),
                    departure_at=datetime.datetime(2025, 8, 21, 9, 45, tzinfo=datetime.timezone.utc),
                    return_at=datetime.datetime(2025, 8, 21, 20, 15, tzinfo=datetime.timezone.utc),
                    duration=450,
                    status="confirmed",
                    seat_class="economy",
                ),
            ],
        ),
        passengers=[
            Passenger(
                id=8,
                gender="string",
                first_name="string",
                second_name="string",
                birth_date=datetime.date(2025, 8, 18),
                passport="string",
                expiration_date=datetime.date(2025, 8, 18),
            )
        ],
    )

    result = await pdf_ticket_adapter.execute(mock_user_ticket)

    assert expected_result == result
