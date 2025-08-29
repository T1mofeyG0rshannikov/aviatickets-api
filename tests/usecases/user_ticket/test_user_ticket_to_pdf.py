import datetime
import uuid
from unittest.mock import MagicMock
from uuid import UUID

import pytest

from src.application.builders.user_ticket import UserTicketFullInfoAssembler
from src.application.dto.airline import AirlineDTO
from src.application.dto.airports.full_info import AirportFullInfoDTO
from src.application.dto.location import CityDTO, CountryDTO, RegionDTO
from src.application.dto.ticket import TicketFullInfoDTO, TicketSegmentFullInfoDTO
from src.application.dto.user import UserDTO
from src.application.dto.user_ticket import (
    AdapterPdfField,
    PassengerDTO,
    UserTicketFullInfoDTO,
)
from src.application.services.currency_converter import CurrencyConverter
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
from src.entities.exceptions import AccessDeniedError
from src.entities.location.country.country import Country
from src.entities.user.user import User
from src.entities.user.value_objects.email import Email
from src.entities.user_ticket.user_ticket import Passenger, UserTicket
from src.entities.user_ticket.value_objects.passport import InternationalPassport
from src.entities.value_objects.entity_id import EntityId
from src.infrastructure.pdf_service.service import PdfService
from src.infrastructure.persistence.dao.tickets_dao import TicketDAO
from src.infrastructure.persistence.repositories.user_repository import UserRepository
from src.infrastructure.persistence.repositories.user_ticket_repository import (
    UserTicketRepository,
)
from src.interface_adapters.file import File
from src.interface_adapters.pdf_templates import PdfTemplatesEnum


@pytest.fixture
def pdf_service() -> PdfService:
    return PdfService()


@pytest.fixture
async def user_ticket_assembler(
    user_repository: UserRepository,
    ticket_dao: TicketDAO,
) -> UserTicketFullInfoAssembler:
    return UserTicketFullInfoAssembler(user_repository, ticket_dao)


@pytest.fixture
def config() -> DefaultPdfTicketAdapterConfig:
    return DefaultPdfTicketAdapterConfig()


@pytest.fixture
async def pdf_ticket_adapter(
    currency_converter: CurrencyConverter,
    config: DefaultPdfTicketAdapterConfig,
) -> DefaultPdfTicketAdapter:
    return DefaultPdfTicketAdapter(config, currency_converter)


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


@pytest.fixture
def mock_assembler() -> UserTicketFullInfoAssembler:
    return MagicMock(spec=UserTicketFullInfoAssembler)


@pytest.fixture
async def mock_create_pdf_ticket(
    default_pdf_generator: DefaultPdfTicketGenerator, mock_user_ticket_repository, mock_assembler
) -> CreatePdfTicket:
    return CreatePdfTicket(
        mock_user_ticket_repository, mock_assembler, strategies={PdfTemplatesEnum.default: default_pdf_generator}
    )


@pytest.mark.asyncio
async def test_create_pdf(mock_create_pdf_ticket: CreatePdfTicket):
    mock_user = User(
        id=EntityId(value=UUID("0c95ad77-07b3-4516-accc-c96647dbbbb8")),
        first_name="Тимофей",
        second_name="Марков",
        email=Email("tgorshannikov@mail.ru"),
        hash_password="$2b$12$nfKvEXfUHAgKZRVPLwwD9.4edFLxtpyTF6SoEvqh2i0Ad4AeyiDQW",
        is_superuser=True,
        is_active=True,
    )

    mock_user_ticket_dto = UserTicketFullInfoDTO(
        id=UUID("b9baccfa-2ddf-4564-808a-0f4eebd6ed6f"),
        user=UserDTO(
            id=UUID("0c95ad77-07b3-4516-accc-c96647dbbbb8"),
            first_name="Тимофей",
            second_name="Марков",
            email="tgorshannikov@mail.ru",
        ),
        ticket=TicketFullInfoDTO(
            id=UUID("fce3917b-2afa-4930-9fed-18b5f79a607d"),
            duration=1505,
            price=4624.6,
            currency="EUR",
            transfers=1,
            segments=[
                TicketSegmentFullInfoDTO(
                    id=UUID("5e699700-d120-4179-9709-803675cbcbb1"),
                    flight_number="MU-248",
                    segment_number=1,
                    destination_airport=AirportFullInfoDTO(
                        id=UUID("52d5275f-ee8f-4ffa-a9f4-f01734198726"),
                        name="Shanghai Pudong International Airport",
                        continent="AS",
                        country=CountryDTO(
                            id=UUID("24f5ae00-c255-4d0b-8d3b-c6706645c48b"),
                            iso="CN",
                            name="Китай",
                            name_english="China",
                        ),
                        region=RegionDTO(
                            id=UUID("9503be6e-a33e-4e2b-a243-843f97b2239a"),
                            iso="CN-31",
                            name="Шанхай",
                            name_english="Shanghai",
                        ),
                        city=CityDTO(
                            id=UUID("8b4e97fd-c6ac-4d08-babf-9c8729a3347c"),
                            name="Шангхаи",
                            name_english="Shanghai (Pudong)",
                        ),
                        scheduled_service="yes",
                        icao="ZSPD",
                        iata="PVG",
                        gps_code="ZSPD",
                        name_russian=None,
                    ),
                    origin_airport=AirportFullInfoDTO(
                        id=UUID("66edf3b0-b9b0-4c66-b180-2bec0fbf0c50"),
                        name="Sheremetyevo International Airport",
                        continent="EU",
                        country=CountryDTO(
                            id=UUID("f942d3f4-cb74-4e04-9b0e-520d553c00bf"),
                            iso="RU",
                            name="Россия",
                            name_english="Russian Federation",
                        ),
                        region=RegionDTO(
                            id=UUID("04d33aae-e413-44f5-b69f-19b3139650a0"),
                            iso="RU-MOS",
                            name="Московская область",
                            name_english="Moskovskaya oblast",
                        ),
                        city=CityDTO(
                            id=UUID("2126dd4b-3744-4ae8-9af0-8098b08fff5f"), name="Москва", name_english="Moscow"
                        ),
                        scheduled_service="yes",
                        icao="UUEE",
                        iata="SVO",
                        gps_code="UUEE",
                        name_russian="Международный аэропорт Шереметьево",
                    ),
                    airline=AirlineDTO(
                        id=UUID("ea29fe9a-7475-4988-8e1e-4b2bd3ee23d8"),
                        iata="MU",
                        icao="CES",
                        name="China Eastern Airlines",
                        name_russian="Чина Еастерн Аирлинес",
                    ),
                    departure_at=datetime.datetime(2025, 8, 25, 11, 50, tzinfo=datetime.timezone.utc),
                    return_at=datetime.datetime(2025, 8, 26, 1, 55, tzinfo=datetime.timezone.utc),
                    duration=545,
                    status="confirmed",
                    seat_class="business",
                ),
                TicketSegmentFullInfoDTO(
                    id=UUID("f546e999-45d2-48a7-9df6-fee8ab80f4b1"),
                    flight_number="MU-245",
                    segment_number=2,
                    destination_airport=AirportFullInfoDTO(
                        id=UUID("7540e008-40b7-4d3c-9ece-5ddeb159eb34"),
                        name="Dubai International Airport",
                        continent="AS",
                        country=CountryDTO(
                            id=UUID("6330f7a0-fc6e-47b5-a918-069568c8a4ed"),
                            iso="AE",
                            name="Объединенные Арабские Эмираты",
                            name_english="United Arab Emirates",
                        ),
                        region=None,
                        city=CityDTO(
                            id=UUID("4ce1f7e4-8a28-4690-a183-9a84d0f2c987"), name="Дубай", name_english="Dubai"
                        ),
                        scheduled_service="yes",
                        icao="OMDB",
                        iata="DXB",
                        gps_code="OMDB",
                        name_russian=None,
                    ),
                    origin_airport=AirportFullInfoDTO(
                        id=UUID("52d5275f-ee8f-4ffa-a9f4-f01734198726"),
                        name="Shanghai Pudong International Airport",
                        continent="AS",
                        country=CountryDTO(
                            id=UUID("24f5ae00-c255-4d0b-8d3b-c6706645c48b"),
                            iso="CN",
                            name="Китай",
                            name_english="China",
                        ),
                        region=RegionDTO(
                            id=UUID("9503be6e-a33e-4e2b-a243-843f97b2239a"),
                            iso="CN-31",
                            name="Шанхай",
                            name_english="Shanghai",
                        ),
                        city=CityDTO(
                            id=UUID("8b4e97fd-c6ac-4d08-babf-9c8729a3347c"),
                            name="Шангхаи",
                            name_english="Shanghai (Pudong)",
                        ),
                        scheduled_service="yes",
                        icao="ZSPD",
                        iata="PVG",
                        gps_code="ZSPD",
                        name_russian=None,
                    ),
                    airline=AirlineDTO(
                        id=UUID("ea29fe9a-7475-4988-8e1e-4b2bd3ee23d8"),
                        iata="MU",
                        icao="CES",
                        name="China Eastern Airlines",
                        name_russian="Чина Еастерн Аирлинес",
                    ),
                    departure_at=datetime.datetime(2025, 8, 26, 7, 45, tzinfo=datetime.timezone.utc),
                    return_at=datetime.datetime(2025, 8, 26, 13, 55, tzinfo=datetime.timezone.utc),
                    duration=610,
                    status="confirmed",
                    seat_class="business",
                ),
            ],
        ),
        passengers=[
            PassengerDTO(
                id=UUID("02cd3d62-ce21-45ed-8d6a-634417219bf8"),
                gender="string",
                first_name="string",
                second_name="string",
            )
        ],
    )
    mock_user_ticket = UserTicket(
        id=EntityId(value=UUID("b9baccfa-2ddf-4564-808a-0f4eebd6ed6f")),
        user_id=EntityId(value=UUID("0c95ad77-07b3-4516-accc-c96647dbbbb8")),
        ticket_id=EntityId(value=UUID("fce3917b-2afa-4930-9fed-18b5f79a607d")),
        passengers=[
            Passenger(
                id=EntityId(UUID("02cd3d62-ce21-45ed-8d6a-634417219bf8")),
                gender="string",
                first_name="string",
                second_name="string",
                birth_date=datetime.datetime(2025, 8, 22, 22, 24, 45, 740000),
                passport=InternationalPassport(number="111111111", expiration_date=datetime.date(2026, 8, 22)),
            )
        ],
    )
    mock_create_pdf_ticket.builder.execute.return_value = mock_user_ticket_dto  # type: ignore
    mock_create_pdf_ticket.user_ticket_repository.get.return_value = mock_user_ticket  # type: ignore

    result = await mock_create_pdf_ticket(user_ticket_id=uuid.uuid4(), user=mock_user)

    assert isinstance(result, File)


@pytest.mark.asyncio
async def test_assecc_denied_create_pdf_ticket(create_pdf_ticket: CreatePdfTicket):
    mock_user = User(
        id=EntityId(value=UUID("0c95be77-07b3-4516-bebe-c96647bebeb8")),
        first_name="Тимофей",
        second_name="Марков",
        email=Email("tgorshannikov@mail.ru"),
        hash_password="$2b$12$nfKvEXfUHAgKZRVPLwwD9.4edFLxtpyTF6SoEvqh2i0Ad4AeyiDQW",
        is_superuser=True,
        is_active=True,
    )
    mock_user_ticket = UserTicket(
        id=EntityId(value=UUID("b9baccfa-2ddf-4564-808a-0f4eebd6ed6f")),
        user_id=EntityId(value=UUID("0c95ad77-07b3-4516-accc-c96647dbbbb8")),
        ticket_id=EntityId(value=UUID("fce3917b-2afa-4930-9fed-18b5f79a607d")),
        passengers=[
            Passenger(
                id=EntityId(value=UUID("02cd3d62-ce21-45ed-8d6a-634417219bf8")),
                gender="string",
                first_name="string",
                second_name="string",
                birth_date=datetime.datetime(2025, 8, 22, 22, 24, 45, 740000),
                passport=InternationalPassport(number="111111111", expiration_date=datetime.date(2026, 8, 22)),
            )
        ],
    )

    create_pdf_ticket.user_ticket_repository = MagicMock(spec=UserTicketRepository)
    create_pdf_ticket.user_ticket_repository.get.return_value = mock_user_ticket

    with pytest.raises(AccessDeniedError) as excinfo:
        await create_pdf_ticket(user_ticket_id=uuid.uuid4(), user=mock_user)

    assert "Вы можете генерировать только свои билеты в pdf" in str(excinfo.value)


@pytest.mark.asyncio
async def test_default_pdf_template_adapter(
    pdf_ticket_adapter: DefaultPdfTicketAdapter, config: DefaultPdfTicketAdapterConfig
):
    expected_result = [
        PdfFieldsAdapter(
            template_name=config.nav_path,
            data_fields_list=[
                [
                    AdapterPdfField(name="reservationCode", value="Not Available"),
                    AdapterPdfField(name="originDateShort", value="25-08-2025"),
                    AdapterPdfField(name="destinationDateShort", value="26-08-2025"),
                    AdapterPdfField(name="fromTo", value="MOSCOW, RUSSIAN FEDERATION - DUBAI, UNITED ARAB EMIRATES"),
                    AdapterPdfField(name="currency", value="RUB"),
                    AdapterPdfField(name="price", value="432,303.45"),
                    AdapterPdfField(name="passengers", value="STRING/STRING\n"),
                ]
            ],
        ),
        PdfFieldsAdapter(
            template_name=config.single_ticket_path,
            data_fields_list=[
                [
                    AdapterPdfField(name="originFlight", value="MU-248"),
                    AdapterPdfField(name="originDepartingTime", value="11:50"),
                    AdapterPdfField(name="originDepartingDate", value="25 AUGUST 2025"),
                    AdapterPdfField(name="originArrivingDate", value="25 Aug 2025"),
                    AdapterPdfField(name="originArrivingTime", value="20:55"),
                    AdapterPdfField(name="Text-AUYa372fuH", value="TUESDAY 26 AUGUST 2025"),
                    AdapterPdfField(name="originDate", value="MONDAY 25 AUGUST 2025"),
                    AdapterPdfField(name="originAirline", value="China Eastern Airlines"),
                    AdapterPdfField(name="originStatus", value="confirmed"),
                    AdapterPdfField(name="originClass", value="business"),
                    AdapterPdfField(name="originAirportAddress", value="MOSCOW, RUSSIAN FEDERATION"),
                    AdapterPdfField(name="originAirport", value="SVO"),
                    AdapterPdfField(name="destinationAirport", value="PVG"),
                    AdapterPdfField(name="destinationAirportAddress", value="SHANGHAI (PUDONG), CHINA"),
                    AdapterPdfField(name="passengers", value="STRING/STRING\n"),
                ],
                [
                    AdapterPdfField(name="originFlight", value="MU-245"),
                    AdapterPdfField(name="originDepartingTime", value="07:45"),
                    AdapterPdfField(name="originDepartingDate", value="26 AUGUST 2025"),
                    AdapterPdfField(name="originArrivingDate", value="26 Aug 2025"),
                    AdapterPdfField(name="originArrivingTime", value="17:55"),
                    AdapterPdfField(name="Text-AUYa372fuH", value="TUESDAY 26 AUGUST 2025"),
                    AdapterPdfField(name="originDate", value="TUESDAY 26 AUGUST 2025"),
                    AdapterPdfField(name="originAirline", value="China Eastern Airlines"),
                    AdapterPdfField(name="originStatus", value="confirmed"),
                    AdapterPdfField(name="originClass", value="business"),
                    AdapterPdfField(name="originAirportAddress", value="SHANGHAI (PUDONG), CHINA"),
                    AdapterPdfField(name="originAirport", value="PVG"),
                    AdapterPdfField(name="destinationAirport", value="DXB"),
                    AdapterPdfField(name="destinationAirportAddress", value="DUBAI, UNITED ARAB EMIRATES"),
                    AdapterPdfField(name="passengers", value="STRING/STRING\n"),
                ],
            ],
        ),
        PdfFieldsAdapter(template_name=config.bottom_path, data_fields_list=[]),
    ]

    mock_user_ticket_dto = UserTicketFullInfoDTO(
        id=UUID("b9baccfa-2ddf-4564-808a-0f4eebd6ed6f"),
        user=UserDTO(
            id=UUID("0c95ad77-07b3-4516-accc-c96647dbbbb8"),
            first_name="Тимофей",
            second_name="Марков",
            email="tgorshannikov@mail.ru",
        ),
        ticket=TicketFullInfoDTO(
            id=UUID("fce3917b-2afa-4930-9fed-18b5f79a607d"),
            duration=1505,
            price=4624.6,
            currency="EUR",
            transfers=1,
            segments=[
                TicketSegmentFullInfoDTO(
                    id=UUID("5e699700-d120-4179-9709-803675cbcbb1"),
                    flight_number="MU-248",
                    segment_number=1,
                    destination_airport=AirportFullInfoDTO(
                        id=UUID("52d5275f-ee8f-4ffa-a9f4-f01734198726"),
                        name="Shanghai Pudong International Airport",
                        continent="AS",
                        country=CountryDTO(
                            id=UUID("24f5ae00-c255-4d0b-8d3b-c6706645c48b"),
                            iso="CN",
                            name="Китай",
                            name_english="China",
                        ),
                        region=RegionDTO(
                            id=UUID("9503be6e-a33e-4e2b-a243-843f97b2239a"),
                            iso="CN-31",
                            name="Шанхай",
                            name_english="Shanghai",
                        ),
                        city=CityDTO(
                            id=UUID("8b4e97fd-c6ac-4d08-babf-9c8729a3347c"),
                            name="Шангхаи",
                            name_english="Shanghai (Pudong)",
                        ),
                        scheduled_service="yes",
                        icao="ZSPD",
                        iata="PVG",
                        gps_code="ZSPD",
                        name_russian=None,
                    ),
                    origin_airport=AirportFullInfoDTO(
                        id=UUID("66edf3b0-b9b0-4c66-b180-2bec0fbf0c50"),
                        name="Sheremetyevo International Airport",
                        continent="EU",
                        country=CountryDTO(
                            id=UUID("f942d3f4-cb74-4e04-9b0e-520d553c00bf"),
                            iso="RU",
                            name="Россия",
                            name_english="Russian Federation",
                        ),
                        region=RegionDTO(
                            id=UUID("04d33aae-e413-44f5-b69f-19b3139650a0"),
                            iso="RU-MOS",
                            name="Московская область",
                            name_english="Moskovskaya oblast",
                        ),
                        city=CityDTO(
                            id=UUID("2126dd4b-3744-4ae8-9af0-8098b08fff5f"), name="Москва", name_english="Moscow"
                        ),
                        scheduled_service="yes",
                        icao="UUEE",
                        iata="SVO",
                        gps_code="UUEE",
                        name_russian="Международный аэропорт Шереметьево",
                    ),
                    airline=AirlineDTO(
                        id=UUID("ea29fe9a-7475-4988-8e1e-4b2bd3ee23d8"),
                        iata="MU",
                        icao="CES",
                        name="China Eastern Airlines",
                        name_russian="Чина Еастерн Аирлинес",
                    ),
                    departure_at=datetime.datetime(2025, 8, 25, 11, 50, tzinfo=datetime.timezone.utc),
                    return_at=datetime.datetime(2025, 8, 26, 1, 55, tzinfo=datetime.timezone.utc),
                    duration=545,
                    status="confirmed",
                    seat_class="business",
                ),
                TicketSegmentFullInfoDTO(
                    id=UUID("f546e999-45d2-48a7-9df6-fee8ab80f4b1"),
                    flight_number="MU-245",
                    segment_number=2,
                    destination_airport=AirportFullInfoDTO(
                        id=UUID("7540e008-40b7-4d3c-9ece-5ddeb159eb34"),
                        name="Dubai International Airport",
                        continent="AS",
                        country=CountryDTO(
                            id=UUID("6330f7a0-fc6e-47b5-a918-069568c8a4ed"),
                            iso="AE",
                            name="Объединенные Арабские Эмираты",
                            name_english="United Arab Emirates",
                        ),
                        region=None,
                        city=CityDTO(
                            id=UUID("4ce1f7e4-8a28-4690-a183-9a84d0f2c987"), name="Дубай", name_english="Dubai"
                        ),
                        scheduled_service="yes",
                        icao="OMDB",
                        iata="DXB",
                        gps_code="OMDB",
                        name_russian=None,
                    ),
                    origin_airport=AirportFullInfoDTO(
                        id=UUID("52d5275f-ee8f-4ffa-a9f4-f01734198726"),
                        name="Shanghai Pudong International Airport",
                        continent="AS",
                        country=CountryDTO(
                            id=UUID("24f5ae00-c255-4d0b-8d3b-c6706645c48b"),
                            iso="CN",
                            name="Китай",
                            name_english="China",
                        ),
                        region=RegionDTO(
                            id=UUID("9503be6e-a33e-4e2b-a243-843f97b2239a"),
                            iso="CN-31",
                            name="Шанхай",
                            name_english="Shanghai",
                        ),
                        city=CityDTO(
                            id=UUID("8b4e97fd-c6ac-4d08-babf-9c8729a3347c"),
                            name="Шангхаи",
                            name_english="Shanghai (Pudong)",
                        ),
                        scheduled_service="yes",
                        icao="ZSPD",
                        iata="PVG",
                        gps_code="ZSPD",
                        name_russian=None,
                    ),
                    airline=AirlineDTO(
                        id=UUID("ea29fe9a-7475-4988-8e1e-4b2bd3ee23d8"),
                        iata="MU",
                        icao="CES",
                        name="China Eastern Airlines",
                        name_russian="Чина Еастерн Аирлинес",
                    ),
                    departure_at=datetime.datetime(2025, 8, 26, 7, 45, tzinfo=datetime.timezone.utc),
                    return_at=datetime.datetime(2025, 8, 26, 13, 55, tzinfo=datetime.timezone.utc),
                    duration=610,
                    status="confirmed",
                    seat_class="business",
                ),
            ],
        ),
        passengers=[
            PassengerDTO(
                id=UUID("02cd3d62-ce21-45ed-8d6a-634417219bf8"),
                gender="string",
                first_name="string",
                second_name="string",
            )
        ],
    )
    result = await pdf_ticket_adapter.execute(mock_user_ticket_dto)

    assert expected_result == result
