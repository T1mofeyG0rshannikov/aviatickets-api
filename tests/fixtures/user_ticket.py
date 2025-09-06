import pytest

from src.application.builders.user_ticket import UserTicketFullInfoAssembler
from src.application.pdf_templates import PdfTemplatesEnum
from src.application.usecases.tickets.pdf.generate import GeneratePdfTicket
from src.application.usecases.tickets.pdf.strategies.default.generator import (
    DefaultPdfTicketGenerator,
)


@pytest.fixture
async def generate_pdf_ticket(
    default_pdf_generator: DefaultPdfTicketGenerator,
    user_ticket_assembler: UserTicketFullInfoAssembler,
) -> GeneratePdfTicket:
    return GeneratePdfTicket(user_ticket_assembler, strategies={PdfTemplatesEnum.default: default_pdf_generator})
