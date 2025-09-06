from src.application.dto.user_ticket import UserTicketFullInfoDTO
from src.application.services.pdf_service import (
    PdfServiceInterface,
    PdfTicketGeneratorStrategy,
)
from src.application.usecases.tickets.pdf.pdf_ticket import PdfTicket
from src.application.usecases.tickets.pdf.strategies.default.adapter import (
    DefaultPdfTicketAdapter,
)


class DefaultPdfTicketGenerator(PdfTicketGeneratorStrategy):
    def __init__(
        self,
        adapter: DefaultPdfTicketAdapter,
        pdf_service: PdfServiceInterface,
    ) -> None:
        self.adapter = adapter
        self.pdf_service = pdf_service

    async def execute(self, user_ticket: UserTicketFullInfoDTO) -> PdfTicket:
        adapter_fields = await self.adapter.execute(user_ticket)

        pdf_segments = []
        for pdf_adapter in adapter_fields:
            if pdf_adapter.data_fields_list:
                for fields in pdf_adapter.data_fields_list:
                    self.pdf_service.set_file(pdf_adapter.template_name)
                    self.pdf_service.update_form(fields)

                    pdf_segments.append(self.pdf_service.save_file())
            else:
                self.pdf_service.set_file(pdf_adapter.template_name)

                pdf_segments.append(self.pdf_service.save_file())

        file_content = self.pdf_service.merge_byte_files(pdf_segments)

        return PdfTicket.from_user_ticket_dto(user_ticket=user_ticket, content=file_content)
