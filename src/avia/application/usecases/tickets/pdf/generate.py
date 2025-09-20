from avia.application.builders.user_ticket import UserTicketFullInfoAssembler
from avia.application.pdf_templates import PdfTemplatesEnum
from avia.application.services.pdf_service import PdfTicketGeneratorStrategy
from avia.application.usecases.tickets.pdf.pdf_ticket import PdfTicket
from avia.entities.user_ticket.user_ticket import UserTicket


class GeneratePdfTicket:
    def __init__(
        self,
        builder: UserTicketFullInfoAssembler,
        strategies: dict[PdfTemplatesEnum, PdfTicketGeneratorStrategy],
    ) -> None:
        self.builder = builder
        self._strategies = strategies

    async def __call__(
        self, user_ticket: UserTicket, template: PdfTemplatesEnum = PdfTemplatesEnum.default
    ) -> PdfTicket:
        user_ticket_dto = await self.builder.execute(user_ticket)
        # print(user_ticket_dto)
        return await self._strategies[template].execute(user_ticket_dto)
