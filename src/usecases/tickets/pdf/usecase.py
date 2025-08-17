from src.dto.file import File
from src.entities.exceptions import AccessDeniedError
from src.entities.user.user import User
from src.entities.user_ticket.exceptions import UserTicketNotFoundError
from src.infrastructure.pdf_service.service import PdfService
from src.infrastructure.repositories.user_ticket_repository import UserTicketRepository
from src.usecases.tickets.filter.dto import TicketFullInfoDTO
from src.usecases.tickets.pdf.adapter import PdfTicketAdapter
from src.usecases.tickets.pdf.builders import UserTicketFullInfoAssembler


class CreatePdfTicket:
    def __init__(
        self,
        adapter: PdfTicketAdapter,
        user_ticket_repository: UserTicketRepository,
        builder: UserTicketFullInfoAssembler,
        pdf_service: PdfService,
    ) -> None:
        self.adapter = adapter
        self.user_ticket_repository = user_ticket_repository
        self.builder = builder
        self.pdf_service = pdf_service

    def get_file_name(self, ticket: TicketFullInfoDTO) -> str:
        return f"{ticket.origin_airport.city.name_english}, {ticket.origin_airport.country.name_english} - {ticket.destination_airport.city.name_english}, {ticket.destination_airport.country.name_english}"

    async def __call__(self, user_ticket_id: int, user: User) -> File:
        user_ticket = await self.user_ticket_repository.get(user_ticket_id)

        if user_ticket is None:
            raise UserTicketNotFoundError(f"Нет пользовательского билета с id='{user_ticket_id}'")

        if user_ticket.user_id != user.id:
            raise AccessDeniedError("Вы можете генерировать только свои билеты в pdf")

        user_ticket_dto = await self.builder.execute(user_ticket)

        adapter_fields = self.adapter.execute(user_ticket_dto)
        print(adapter_fields)

        self.pdf_service.set_file(r"C:\Users\tgors\Desktop\ticket-template2.pdf")

        self.pdf_service.update_form(adapter_fields)

        file_content = self.pdf_service.save_file()

        return File(name=self.get_file_name(user_ticket_dto.ticket), content=file_content)
