from src.application.dto.pdf_service import AdapterPdfField
from src.application.services.currency_converter import CurrencyConverter
from src.application.services.pdf_service import PdfServiceInterface
from src.application.usecases.insurance.config import PdfInsuranceGeneratorConfig
from src.application.usecases.insurance.pdf_insurance import PdfInsurance
from src.entities.insurance.insurance import Insurance
from src.entities.user.exceptions import UserNotFoundError
from src.entities.user.user_repository import UserRepositoryInterface
from src.entities.value_objects.price.currency_enum import CurrencyEnum


class PdfInsuranceAdapter:
    def __init__(self, currency_converter: CurrencyConverter, user_repository: UserRepositoryInterface) -> None:
        self.currency_converter = currency_converter
        self.user_repository = user_repository

    async def get_premium(self, insurance: Insurance) -> str:
        premium_rub = await self.currency_converter.to_rub(insurance.premium.currency, insurance.premium.value)
        return f"""{insurance.premium.value} {insurance.premium.currency} / {premium_rub} {CurrencyEnum.rub}"""

    async def execute(self, insurance: Insurance) -> list[AdapterPdfField]:
        premium = await self.get_premium(insurance)

        insured = await self.user_repository.get(id=insurance.insured_id)

        if insured is None:
            raise UserNotFoundError(f"Нет пользователя с id='{insurance.insured_id}'")

        return [
            AdapterPdfField(name="Days", value=str(insurance.length_of_stay)),
            AdapterPdfField(name="Contract", value=str(insurance.contract)),
            AdapterPdfField(name="Insured", value=insured.full_name.upper()),
            AdapterPdfField(name="InsuredEng", value=str(insurance.length_of_stay)),
            AdapterPdfField(name="Territory", value=str(insurance.length_of_stay)),
            AdapterPdfField(name="CreatedAt", value=insurance.created_at.strftime("%d.%m.%Y")),
            AdapterPdfField(name="FromDate", value=insurance.start_date.strftime("%d.%m.%Y")),
            AdapterPdfField(name="ToDate", value=insurance.end_date.strftime("%d.%m.%Y")),
            AdapterPdfField(name="Premium", value=premium),
        ]


class GeneratePdfInsuranse:
    def __init__(
        self, config: PdfInsuranceGeneratorConfig, adapter: PdfInsuranceAdapter, pdf_service: PdfServiceInterface
    ) -> None:
        self.adapter = adapter
        self.pdf_service = pdf_service
        self.config = config

    async def __call__(self, insurance: Insurance) -> PdfInsurance:
        adapter_fields = await self.adapter.execute(insurance)

        self.pdf_service.set_file(self.config.template_name)

        self.pdf_service.update_form(adapter_fields)

        file_content = self.pdf_service.save_file()

        return PdfInsurance.from_insurance(insurance=insurance, content=file_content)
