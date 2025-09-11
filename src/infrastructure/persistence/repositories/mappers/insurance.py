from src.entities.insurance.insurance import Insurance
from src.entities.insurance.value_objects.contract import InsuranceContract
from src.entities.user.value_objects.user_id import UserId
from src.entities.value_objects.entity_id import EntityId
from src.entities.value_objects.price.price import Price
from src.infrastructure.persistence.db.models.models import InsuranceOrm


def orm_to_insurance(insurance: InsuranceOrm) -> Insurance:
    return Insurance(
        id=EntityId(insurance.id),
        contract=InsuranceContract(insurance.contract),
        insured_id=UserId(insurance.insured_id),
        premium=Price(value=insurance.premium_value, currency=insurance.premium_currency),
        created_at=insurance.created_at,
        start_date=insurance.start_date,
        end_date=insurance.end_date,
        length_of_stay=(insurance.end_date - insurance.start_date).days,
        territory=insurance.territory,
    )
