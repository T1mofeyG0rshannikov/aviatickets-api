from src.entities.user_ticket.user_ticket import Passenger
from src.infrastructure.db.models.models import PassengerOrm


def from_orm_to_passenger(passenger: PassengerOrm) -> Passenger:
    return Passenger(
        id=passenger.id,
        gender=passenger.gender,
        first_name=passenger.first_name,
        second_name=passenger.second_name,
        birth_date=passenger.birth_date,
        passport=passenger.passport,
        expiration_date=passenger.expiration_date,
    )
