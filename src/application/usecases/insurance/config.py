from pydantic import Field
from pydantic_settings import BaseSettings


class PdfInsuranceGeneratorConfig(BaseSettings):
    template_name = Field(alias="INSURANCE_PDF_TEMPLATE_PATH")

    class Config:
        extra = "allow"
        env_file = ".env"
