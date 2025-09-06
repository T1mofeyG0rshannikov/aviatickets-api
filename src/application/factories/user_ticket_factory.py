from datetime import date, datetime

from src.application.dto.user_ticket import CreatePassengerDTO
from src.entities.user.value_objects.user_id import UserId
from src.entities.user_ticket.exceptions import (
    ExpiredInternationalPassportError,
    InvalidInternationalPassportError,
)
from src.entities.user_ticket.user_ticket import Passenger, UserTicket
from src.entities.user_ticket.value_objects.passport import InternationalPassport
from src.entities.value_objects.entity_id import EntityId


class PassengerFactory:
    @classmethod
    def create(
        cls,
        gender: str,
        first_name: str,
        second_name: str,
        birth_date: datetime,
        passport_number: str,
        passport_expiration_date: date,
    ) -> Passenger:
        try:
            return Passenger.create(
                gender=gender,
                first_name=first_name,
                second_name=second_name,
                birth_date=birth_date,
                passport=InternationalPassport(number=passport_number, expiration_date=passport_expiration_date),
            )
        except InvalidInternationalPassportError:
            raise InvalidInternationalPassportError(
                f"{first_name} {second_name}: Неправильный номер загран паспорта - {passport_number}"
            )

        except ExpiredInternationalPassportError:
            raise ExpiredInternationalPassportError(
                f"У пассажира {first_name} {second_name} истёк срок загран. паспорта"
            )


class UserTicketFactory:
    @classmethod
    def create(cls, user_id: UserId, ticket_id: EntityId, passengers_dto: list[CreatePassengerDTO]) -> UserTicket:
        passengers = []

        for passenger in passengers_dto:
            passengers.append(
                PassengerFactory.create(
                    gender=passenger.gender,
                    first_name=passenger.first_name,
                    second_name=passenger.second_name,
                    birth_date=passenger.birth_date,
                    passport_number=passenger.passport,
                    passport_expiration_date=passenger.expiration_date,
                )
            )

        return UserTicket.create(user_id=user_id, ticket_id=ticket_id, passengers=passengers)
