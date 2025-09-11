from dataclasses import dataclass
from datetime import datetime

from src.entities.insurance.value_objects.contract import InsuranceContract
from src.entities.tickets.ticket_entity.ticket import Ticket
from src.entities.user.value_objects.user_id import UserId
from src.entities.value_objects.entity_id import EntityId
from src.entities.value_objects.price.currency_enum import CurrencyEnum
from src.entities.value_objects.price.price import Price


@dataclass
class Insurance:
    id: EntityId
    contract: InsuranceContract
    insured_id: UserId
    premium: Price
    created_at: datetime
    start_date: datetime
    end_date: datetime
    length_of_stay: int
    territory: str

    @classmethod
    def create(cls, insured_id: UserId, ticket: Ticket, territory: str):
        start_date = ticket.departure_date

        end_date = ticket.arrival_date

        length_of_stay = (end_date - start_date).days

        return cls(
            id=EntityId.generate(),
            contract=InsuranceContract.generate(),
            insured_id=insured_id,
            created_at=datetime.today(),
            premium=Price(value=length_of_stay * 1.14, currency=CurrencyEnum.usd),
            start_date=start_date,
            end_date=end_date,
            length_of_stay=length_of_stay,
            territory=territory,
        )
