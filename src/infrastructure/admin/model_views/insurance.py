from src.infrastructure.admin.model_views.base import BaseModelView
from src.infrastructure.persistence.db.models.models import (
    InsuranceOrm,
    PdfInsuranceOrm,
)


class InsuranceAdmin(BaseModelView, model=InsuranceOrm):  # type: ignore
    column_list = [
        InsuranceOrm.id,
        InsuranceOrm.contract,
        InsuranceOrm.insured_id,
        InsuranceOrm.insured,
        InsuranceOrm.premium_value,
        InsuranceOrm.premium_currency,
        InsuranceOrm.created_at,
        InsuranceOrm.start_date,
        InsuranceOrm.end_date,
        InsuranceOrm.territory,
    ]

    page_size = 100
    list_template = "sqladmin/list-countries.html"

    name = "Страховка"
    name_plural = "Страховки"

    column_default_sort = ("id", "desc")


class InsurancePdfAdmin(BaseModelView, model=PdfInsuranceOrm):  # type: ignore
    column_list = [PdfInsuranceOrm.id, PdfInsuranceOrm.insurance, PdfInsuranceOrm.name, PdfInsuranceOrm.content_path]
