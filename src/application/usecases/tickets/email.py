from src.application.usecases.tickets.pdf.usecase import CreatePdfTicket
from src.entities.exceptions import AccessDeniedError
from src.entities.user.user import User
from src.entities.user_ticket.exceptions import UserTicketNotFoundError
from src.infrastructure.email_sender.service import EmailSender
from src.infrastructure.repositories.user_ticket_repository import UserTicketRepository


class SendPdfTicketToEmail:
    def __init__(
        self,
        user_ticket_repository: UserTicketRepository,
        create_pdf_ticket: CreatePdfTicket,
        email_sender: EmailSender,
    ) -> None:
        self.create_pdf_ticket = create_pdf_ticket
        self.email_sender = email_sender
        self.repository = user_ticket_repository

    async def __call__(self, user_ticket_id: int, user: User) -> None:
        user_ticket = await self.repository.get(id=user_ticket_id)
        if user_ticket is None:
            raise UserTicketNotFoundError(f"Нет пользовательского билета с id='{user_ticket_id}'")

        if user_ticket.user_id != user.id:
            raise AccessDeniedError("Вы можете получать на почту только свои билеты")

        file = await self.create_pdf_ticket(user_ticket_id=user_ticket_id, user=user)
        self.email_sender.send(
            recipient_email=user.email, subject="Электронный билет", body="Вот ваш билет", files=[file]
        )
