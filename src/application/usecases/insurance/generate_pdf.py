from src.application.dto.pdf_service import AdapterPdfField
from src.application.services.pdf_service import PdfServiceInterface
from src.application.usecases.insurance.config import PdfInsuranceGeneratorConfig
from src.entities.insurance.insurance import Insurance
from src.interface_adapters.file import File


class PdfInsuranceAdapter:
    def execute(self, insurance: Insurance) -> list[AdapterPdfField]:
        return [AdapterPdfField(name="length_of_stay", value=str(insurance.length_of_stay))]


class GeneratePdfInsuranse:
    def __init__(
        self, config: PdfInsuranceGeneratorConfig, adapter: PdfInsuranceAdapter, pdf_service: PdfServiceInterface
    ) -> None:
        self.adapter = adapter
        self.pdf_service = pdf_service
        self.config = config

    def get_file_name(self) -> str:
        return "insurance"

    async def __call__(self, insurance: Insurance) -> File:
        adapter_fields = self.adapter.execute(insurance)

        self.pdf_service.set_file(self.config.template_name)

        self.pdf_service.update_form(adapter_fields)

        file_content = self.pdf_service.save_file()

        return File(name=self.get_file_name(), content=file_content)
