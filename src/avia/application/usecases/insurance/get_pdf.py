from avia.application.persistence.data_mappers.insurance_files import (
    InsuranceFilesDataMapperInterface,
)
from avia.application.persistence.transaction import Transaction
from avia.application.services.file_manager import FileManagerInterface
from avia.application.usecases.insurance.exceptions import InsuranceFileNotFoundError
from avia.application.usecases.insurance.generate_pdf import GeneratePdfInsuranse
from avia.application.usecases.insurance.pdf_insurance import PdfInsurance
from avia.application.usecases.tickets.pdf.config import PdfGeneratorConfig
from avia.entities.exceptions import AccessDeniedError
from avia.entities.insurance.exceptions import InsuranceNotFoundError
from avia.entities.insurance.repository import InsuranceRepositoryInterface
from avia.entities.user.user import User
from avia.entities.value_objects.entity_id import EntityId


class GetPdfInsurance:
    def __init__(
        self,
        transaction: Transaction,
        file_manager: FileManagerInterface,
        generate_pdf: GeneratePdfInsuranse,
        ticket_files_data_mapper: InsuranceFilesDataMapperInterface,
        repository: InsuranceRepositoryInterface,
        config: PdfGeneratorConfig,
    ) -> None:
        self.file_manager = file_manager
        self.generate_pdf = generate_pdf
        self.data_mapper = ticket_files_data_mapper
        self.repository = repository
        self.config = config
        self.transaction = transaction

    async def __call__(self, insurance_id: EntityId, user: User) -> PdfInsurance:
        insurance = await self.repository.get(insurance_id)

        if insurance is None:
            raise InsuranceNotFoundError(f"Нет страховки с id='{insurance_id}'")

        if insurance.insured_id != user.id:
            raise AccessDeniedError("Вы можете получать только свои страховки в pdf")

        db_pdf_insurance = await self.data_mapper.get_insurance_file(insurance_id)

        if db_pdf_insurance is not None:
            pdf_insurance_file = self.file_manager.find_by_name(
                folder=self.config.pdf_tickets_folder, file_name=db_pdf_insurance.name
            )

            if pdf_insurance_file is None:
                raise InsuranceFileNotFoundError(f"Нет pdf для страховки с id = '{insurance_id}'")

            return PdfInsurance(name=db_pdf_insurance.name, content=pdf_insurance_file.content)

        pdf_insurance = await self.generate_pdf(insurance)
        self.file_manager.save(folder=self.config.pdf_insurance_folder, file=pdf_insurance)

        content_path = f"{self.config.pdf_tickets_folder}/{pdf_insurance.name}"
        await self.data_mapper.save(name=pdf_insurance.name, insurance_id=insurance_id, content_path=content_path)
        await self.transaction.commit()
        return pdf_insurance
