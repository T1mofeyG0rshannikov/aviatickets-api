from unittest.mock import MagicMock

import mocks
import pytest

from src.application.builders.user_ticket import UserTicketFullInfoAssembler
from src.application.dto.pdf_service import AdapterPdfField
from src.application.pdf_templates import PdfTemplatesEnum
from src.application.services.currency_converter import CurrencyConverter
from src.application.usecases.tickets.pdf.generate import GeneratePdfTicket
from src.application.usecases.tickets.pdf.pdf_ticket import PdfTicket
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
from src.entities.user_ticket.user_ticket import UserTicket
from src.infrastructure.pdf_service.service import PdfService
from src.infrastructure.persistence.dao.tickets_dao import TicketDAO
from src.infrastructure.persistence.repositories.user_repository import UserRepository


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
async def generate_pdf_ticket(
    default_pdf_generator: DefaultPdfTicketGenerator,
    user_ticket_assembler: UserTicketFullInfoAssembler,
) -> GeneratePdfTicket:
    return GeneratePdfTicket(user_ticket_assembler, strategies={PdfTemplatesEnum.default: default_pdf_generator})


@pytest.fixture
def mock_assembler() -> UserTicketFullInfoAssembler:
    return MagicMock(spec=UserTicketFullInfoAssembler)


@pytest.fixture
async def mock_create_pdf_ticket(default_pdf_generator: DefaultPdfTicketGenerator, mock_assembler) -> GeneratePdfTicket:
    return GeneratePdfTicket(mock_assembler, strategies={PdfTemplatesEnum.default: default_pdf_generator})


@pytest.mark.asyncio
async def test_create_pdf(mock_create_pdf_ticket: GeneratePdfTicket):
    mock_user_ticket_dto = mocks.mock_user_ticket_dto

    mock_create_pdf_ticket.builder.execute.return_value = mock_user_ticket_dto  # type: ignore

    mock_user_ticket = MagicMock(spec=UserTicket)

    result = await mock_create_pdf_ticket(user_ticket=mock_user_ticket)

    assert isinstance(result, PdfTicket)


@pytest.mark.asyncio
async def test_default_pdf_template_adapter(
    pdf_ticket_adapter: DefaultPdfTicketAdapter, config: DefaultPdfTicketAdapterConfig
):
    mock_user_ticket_dto = mocks.mock_user_ticket_dto

    expected_result = [
        PdfFieldsAdapter(
            template_name="C:/Users/tgors/Desktop/top.pdf",
            data_fields_list=[
                [
                    AdapterPdfField(name="reservationCode", value="Not Available"),
                    AdapterPdfField(name="originDateShort", value="04-09-2025"),
                    AdapterPdfField(name="destinationDateShort", value="04-09-2025"),
                    AdapterPdfField(name="fromTo", value="MOSCOW, RUSSIA - MOSCOW, RUSSIA"),
                    AdapterPdfField(name="currency", value="RUB"),
                    AdapterPdfField(name="price", value="89,891.37"),
                    AdapterPdfField(name="passengers", value="STRING/STRING\n"),
                ]
            ],
        ),
        PdfFieldsAdapter(
            template_name="C:/Users/tgors/Desktop/new-single-ticket.pdf",
            data_fields_list=[
                [
                    AdapterPdfField(name="originFlight", value="QR-340"),
                    AdapterPdfField(name="originDepartingTime", value="14:05"),
                    AdapterPdfField(name="originDepartingDate", value="04 SEPTEMBER 2025"),
                    AdapterPdfField(name="originArrivingDate", value="04 Sep 2025"),
                    AdapterPdfField(name="originArrivingTime", value="19:30"),
                    AdapterPdfField(name="Text-AUYa372fuH", value="THURSDAY 04 SEPTEMBER 2025"),
                    AdapterPdfField(name="originDate", value="THURSDAY 04 SEPTEMBER 2025"),
                    AdapterPdfField(name="originAirline", value="Qatar Airways"),
                    AdapterPdfField(name="originStatus", value="confirmed"),
                    AdapterPdfField(name="originClass", value="premium economy"),
                    AdapterPdfField(name="originAirportAddress", value="MOSCOW, RUSSIA"),
                    AdapterPdfField(name="originAirport", value="SVO"),
                    AdapterPdfField(name="destinationAirport", value="DOH"),
                    AdapterPdfField(name="destinationAirportAddress", value="DOHA, QATAR"),
                    AdapterPdfField(name="passengers", value="STRING/STRING\n"),
                ],
                [
                    AdapterPdfField(name="originFlight", value="QR-1002"),
                    AdapterPdfField(name="originDepartingTime", value="22:15"),
                    AdapterPdfField(name="originDepartingDate", value="04 SEPTEMBER 2025"),
                    AdapterPdfField(name="originArrivingDate", value="04 Sep 2025"),
                    AdapterPdfField(name="originArrivingTime", value="23:35"),
                    AdapterPdfField(name="Text-AUYa372fuH", value="THURSDAY 04 SEPTEMBER 2025"),
                    AdapterPdfField(name="originDate", value="THURSDAY 04 SEPTEMBER 2025"),
                    AdapterPdfField(name="originAirline", value="Qatar Airways"),
                    AdapterPdfField(name="originStatus", value="confirmed"),
                    AdapterPdfField(name="originClass", value="premium economy"),
                    AdapterPdfField(name="originAirportAddress", value="DOHA, QATAR"),
                    AdapterPdfField(name="originAirport", value="DOH"),
                    AdapterPdfField(name="destinationAirport", value="DXB"),
                    AdapterPdfField(name="destinationAirportAddress", value="DUBAI, UNITED ARAB EMIRATES"),
                    AdapterPdfField(name="passengers", value="STRING/STRING\n"),
                ],
                [
                    AdapterPdfField(name="originFlight", value="QR-1023"),
                    AdapterPdfField(name="originDepartingTime", value="09:15"),
                    AdapterPdfField(name="originDepartingDate", value="10 SEPTEMBER 2025"),
                    AdapterPdfField(name="originArrivingDate", value="10 Sep 2025"),
                    AdapterPdfField(name="originArrivingTime", value="10:30"),
                    AdapterPdfField(name="Text-AUYa372fuH", value="WEDNESDAY 10 SEPTEMBER 2025"),
                    AdapterPdfField(name="originDate", value="WEDNESDAY 10 SEPTEMBER 2025"),
                    AdapterPdfField(name="originAirline", value="Qatar Airways"),
                    AdapterPdfField(name="originStatus", value="confirmed"),
                    AdapterPdfField(name="originClass", value="premium economy"),
                    AdapterPdfField(name="originAirportAddress", value="DUBAI, UNITED ARAB EMIRATES"),
                    AdapterPdfField(name="originAirport", value="DXB"),
                    AdapterPdfField(name="destinationAirport", value="DOH"),
                    AdapterPdfField(name="destinationAirportAddress", value="DOHA, QATAR"),
                    AdapterPdfField(name="passengers", value="STRING/STRING\n"),
                ],
                [
                    AdapterPdfField(name="originFlight", value="QR-337"),
                    AdapterPdfField(name="originDepartingTime", value="12:50"),
                    AdapterPdfField(name="originDepartingDate", value="10 SEPTEMBER 2025"),
                    AdapterPdfField(name="originArrivingDate", value="10 Sep 2025"),
                    AdapterPdfField(name="originArrivingTime", value="18:20"),
                    AdapterPdfField(name="Text-AUYa372fuH", value="WEDNESDAY 10 SEPTEMBER 2025"),
                    AdapterPdfField(name="originDate", value="WEDNESDAY 10 SEPTEMBER 2025"),
                    AdapterPdfField(name="originAirline", value="Qatar Airways"),
                    AdapterPdfField(name="originStatus", value="confirmed"),
                    AdapterPdfField(name="originClass", value="premium economy"),
                    AdapterPdfField(name="originAirportAddress", value="DOHA, QATAR"),
                    AdapterPdfField(name="originAirport", value="DOH"),
                    AdapterPdfField(name="destinationAirport", value="SVO"),
                    AdapterPdfField(name="destinationAirportAddress", value="MOSCOW, RUSSIA"),
                    AdapterPdfField(name="passengers", value="STRING/STRING\n"),
                ],
            ],
        ),
        PdfFieldsAdapter(template_name="C:/Users/tgors/Desktop/bottom.pdf", data_fields_list=[]),
    ]

    result = await pdf_ticket_adapter.execute(mock_user_ticket_dto)

    assert expected_result == result
