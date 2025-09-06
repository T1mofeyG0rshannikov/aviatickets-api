from src.application.persistence.data_mappers.ticket_files import (
    TicketFilesDataMapperInterface,
)
from src.application.services.file_manager import FileManagerInterface
from src.application.usecases.tickets.pdf.config import PdfGeneratorConfig
from src.application.usecases.tickets.pdf.exceptions import TicketFileNotFoundError
from src.application.usecases.tickets.pdf.generate import GeneratePdfTicket
from src.application.usecases.tickets.pdf.pdf_ticket import PdfTicket
from src.entities.exceptions import AccessDeniedError
from src.entities.user.user import User
from src.entities.user_ticket.exceptions import UserTicketNotFoundError
from src.entities.user_ticket.user_ticket_repository import (
    UserTicketRepositoryInterface,
)
from src.entities.value_objects.entity_id import EntityId


class GetPdfTicket:
    def __init__(
        self,
        file_manager: FileManagerInterface,
        generate_pdf: GeneratePdfTicket,
        ticket_files_data_mapper: TicketFilesDataMapperInterface,
        user_ticket_repository: UserTicketRepositoryInterface,
        config: PdfGeneratorConfig,
    ) -> None:
        self.file_manager = file_manager
        self.generate_pdf = generate_pdf
        self.data_mapper = ticket_files_data_mapper
        self.user_ticket_repository = user_ticket_repository
        self.config = config

    async def __call__(self, user_ticket_id: EntityId, user: User) -> PdfTicket:
        user_ticket = await self.user_ticket_repository.get(user_ticket_id)

        if user_ticket is None:
            raise UserTicketNotFoundError(f"Нет пользовательского билета с id='{user_ticket_id}'")

        if user_ticket.user_id != user.id:
            raise AccessDeniedError("Вы можете получать только свои билеты в pdf")

        db_pdf_ticket = await self.data_mapper.get_user_ticket_file(user_ticket_id)

        if db_pdf_ticket is not None:
            pdf_ticket_file = self.file_manager.find_by_name(
                folder=self.config.pdf_tickets_folder, file_name=db_pdf_ticket.name
            )

            if pdf_ticket_file is None:
                raise TicketFileNotFoundError(f"Нет pdf билета для пользовательского билета с id = '{user_ticket_id}'")

            return PdfTicket(name=db_pdf_ticket.name, content=pdf_ticket_file.content)

        pdf_ticket = await self.generate_pdf(user_ticket)
        self.file_manager.save(folder=self.config.pdf_tickets_folder, file=pdf_ticket)

        content_path = f"{self.config.pdf_tickets_folder}/{pdf_ticket.name}.pdf"
        await self.data_mapper.save(name=pdf_ticket.name, user_ticket_id=user_ticket_id, content_path=content_path)
        return pdf_ticket
