from datetime import date
from unittest.mock import MagicMock
from uuid import UUID

import pytest

from src.application.builders.user_ticket import UserTicketFullInfoAssembler
from src.application.pdf_templates import PdfTemplatesEnum
from src.application.persistence.data_mappers.ticket_files import (
    TicketFilesDataMapperInterface,
)
from src.application.services.currency_converter import CurrencyConverter
from src.application.services.file_manager import FileManagerInterface
from src.application.usecases.tickets.pdf.config import PdfGeneratorConfig
from src.application.usecases.tickets.pdf.generate import GeneratePdfTicket
from src.application.usecases.tickets.pdf.get import GetPdfTicket
from src.application.usecases.tickets.pdf.strategies.default.adapter import (
    DefaultPdfTicketAdapter,
)
from src.application.usecases.tickets.pdf.strategies.default.config import (
    DefaultPdfTicketAdapterConfig,
)
from src.application.usecases.tickets.pdf.strategies.default.generator import (
    DefaultPdfTicketGenerator,
)
from src.entities.exceptions import AccessDeniedError
from src.entities.user.user import User
from src.entities.user.value_objects.birth_date import BirthDate
from src.entities.user.value_objects.email import Email
from src.entities.user.value_objects.first_name import FirstName
from src.entities.user.value_objects.second_name import SecondName
from src.entities.user.value_objects.user_id import UserId
from src.entities.user_ticket.user_ticket import UserTicket
from src.entities.user_ticket.user_ticket_repository import (
    UserTicketRepositoryInterface,
)
from src.entities.value_objects.entity_id import EntityId
from src.infrastructure.pdf_service.service import PdfService
from src.infrastructure.persistence.dao.tickets_dao import TicketDAO
from src.infrastructure.persistence.data_mappers.ticket_files_data_mapper import (
    TicketFilesDataMapper,
)
from src.infrastructure.persistence.repositories.user_repository import UserRepository
from src.infrastructure.persistence.repositories.user_ticket_repository import (
    UserTicketRepository,
)


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
def ticket_files_data_mapper() -> TicketFilesDataMapper:
    return MagicMock(spec=TicketFilesDataMapper)


@pytest.fixture
def pdf_generator_config() -> PdfGeneratorConfig:
    return PdfGeneratorConfig()


@pytest.fixture
async def get_pdf_ticket(
    file_manager: FileManagerInterface,
    generate_pdf_ticket: GeneratePdfTicket,
    ticket_files_data_mapper: TicketFilesDataMapperInterface,
    user_ticket_repository: UserTicketRepositoryInterface,
    pdf_generator_config: PdfGeneratorConfig,
) -> GetPdfTicket:
    return GetPdfTicket(
        file_manager, generate_pdf_ticket, ticket_files_data_mapper, user_ticket_repository, pdf_generator_config
    )


@pytest.fixture
def mock_assembler() -> UserTicketFullInfoAssembler:
    return MagicMock(spec=UserTicketFullInfoAssembler)


@pytest.fixture
async def mock_create_pdf_ticket(
    default_pdf_generator: DefaultPdfTicketGenerator, mock_assembler: UserTicketFullInfoAssembler
) -> GeneratePdfTicket:
    return GeneratePdfTicket(mock_assembler, strategies={PdfTemplatesEnum.default: default_pdf_generator})


@pytest.mark.asyncio
async def test_assecc_denied_create_pdf_ticket(get_pdf_ticket: GetPdfTicket):
    mock_user = User(
        id=UserId(value=UUID("0c95be77-07b3-4516-bebe-c96647bebeb8")),
        first_name=FirstName("Тимофей"),
        second_name=SecondName("Марков"),
        email=Email("tgorshannikov@mail.ru"),
        hash_password="$2b$12$nfKvEXfUHAgKZRVPLwwD9.4edFLxtpyTF6SoEvqh2i0Ad4AeyiDQW",
        birth_date=BirthDate(value=date(2000, 1, 1)),
        is_superuser=True,
        is_active=True,
    )

    mock_user_ticket = MagicMock(spec=UserTicket)
    mock_user_ticket.user_id = UserId(value=UUID("0c95ad77-07b3-4516-accc-c96647dbbbb8"))

    get_pdf_ticket.user_ticket_repository = MagicMock(spec=UserTicketRepository)
    get_pdf_ticket.user_ticket_repository.get.return_value = mock_user_ticket

    with pytest.raises(AccessDeniedError) as excinfo:
        await get_pdf_ticket(
            user_ticket_id=EntityId(value=UUID("b9baccfa-2ddf-4564-808a-0f4eebd6ed6f")), user=mock_user
        )
    print(str(excinfo.value), "Error")
    assert "Вы можете получать только свои билеты в pdf" in str(excinfo.value)
