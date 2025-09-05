from dataclasses import dataclass
from datetime import datetime

from src.entities.tickets.ticket_entity.ticket import Ticket
from src.entities.value_objects.entity_id import EntityId
from src.entities.value_objects.price.currency_enum import CurrencyEnum
from src.entities.value_objects.price.price import Price


@dataclass
class Insurance:
    id: EntityId
    owner_id: EntityId
    coverage_amount: Price
    created_at: datetime
    start_date: datetime
    end_date: datetime
    length_of_stay: int

    @classmethod
    def create(cls, owner_id: EntityId, ticket: Ticket):
        start_date = ticket.departure_date

        end_date = ticket.arrival_date

        length_of_stay = (end_date - start_date).days

        return cls(
            id=EntityId.generate(),
            owner_id=owner_id,
            created_at=datetime.today(),
            coverage_amount=Price(value=length_of_stay * 1.14, currency=CurrencyEnum.usd),
            start_date=start_date,
            end_date=end_date,
            length_of_stay=length_of_stay,
        )
