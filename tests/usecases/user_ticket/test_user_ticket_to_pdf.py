import datetime
from unittest.mock import MagicMock

import pytest

from src.dto.file import File
from src.entities.exceptions import AccessDeniedError
from src.entities.user_ticket.dto import CreatePassengerDTO
from src.entities.user_ticket.user_ticket import UserTicket
from src.infrastructure.pdf_service.service import PdfService
from src.infrastructure.repositories.user_repository import UserRepository
from src.infrastructure.repositories.user_ticket_repository import UserTicketRepository
from src.usecases.create_user_ticket.usecase import CreateUserTicket
from src.usecases.tickets.filter.repository.tickets_repository import (
    TicketReadRepository,
)
from src.usecases.tickets.pdf.adapter import PdfTicketAdapter
from src.usecases.tickets.pdf.builders import UserTicketFullInfoAssembler
from src.usecases.tickets.pdf.usecase import CreatePdfTicket


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
def pdf_ticket_adapter() -> PdfTicketAdapter:
    return PdfTicketAdapter()


@pytest.fixture
async def mock_user_ticket_repository(db):
    return UserTicketRepository(db)


@pytest.fixture
async def create_pdf_ticket(
    pdf_ticket_adapter: PdfTicketAdapter,
    user_ticket_repository: UserTicketRepository,
    user_ticket_assembler: UserTicketFullInfoAssembler,
    pdf_service: PdfService,
) -> CreatePdfTicket:
    return CreatePdfTicket(pdf_ticket_adapter, user_ticket_repository, user_ticket_assembler, pdf_service)


@pytest.mark.asyncio
async def test_create_pdf(
    create_pdf_ticket: CreatePdfTicket, user_repository: UserRepository, create_user_ticket: CreateUserTicket
):
    user = await user_repository.get(id=2)

    await create_user_ticket(
        ticket_id=1,
        passangers=[
            CreatePassengerDTO(
                first_name="Тимофей",
                second_name="Марков",
                gender="Мужской",
                birth_date=datetime.datetime(year=2025, month=1, day=1),
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
