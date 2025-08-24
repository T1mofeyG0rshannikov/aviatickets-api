from src.entities.user_ticket.user_ticket import Passenger
from src.entities.user_ticket.value_objects.passport import InternationalPassport
from src.entities.value_objects.entity_id import EntityId
from src.infrastructure.persistence.db.models.models import PassengerOrm


def from_orm_to_passenger(passenger: PassengerOrm) -> Passenger:
    return Passenger(
        id=EntityId(passenger.id),
        gender=passenger.gender,
        first_name=passenger.first_name,
        second_name=passenger.second_name,
        birth_date=passenger.birth_date,
        passport=InternationalPassport(
            passenger.passport,
            expiration_date=passenger.expiration_date,
        ),
    )
