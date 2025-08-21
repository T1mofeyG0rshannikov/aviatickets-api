from src.application.dto.ticket import TicketFullInfoDTO
from src.application.dto.user_ticket import UserTicketFullInfoDTO
from src.application.usecases.tickets.pdf.strategies.base import (
    PdfTicketGeneratorStrategy,
)
from src.application.usecases.tickets.pdf.strategies.default.adapter import (
    DefaultPdfTicketAdapter,
)
from src.infrastructure.pdf_service.service import PdfService
from src.interface_adapters.file import File


class DefaultPdfTicketGenerator(PdfTicketGeneratorStrategy):
    def __init__(
        self,
        adapter: DefaultPdfTicketAdapter,
        pdf_service: PdfService,
    ) -> None:
        self.adapter = adapter
        self.pdf_service = pdf_service

    def get_file_name(self, ticket: TicketFullInfoDTO) -> str:
        return f"{ticket.segments[0].origin_airport.city.name_english}_{ticket.segments[0].origin_airport.country.name_english}-{ticket.segments[-1].destination_airport.city.name_english}_{ticket.segments[-1].destination_airport.country.name_english}"

    async def execute(self, user_ticket: UserTicketFullInfoDTO) -> File:
        adapter_fields = await self.adapter.execute(user_ticket)
        print(adapter_fields)
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

        return File(name=self.get_file_name(user_ticket.ticket), content=file_content)
