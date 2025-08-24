from uuid import UUID

from src.application.dto.user_ticket import CreatePassengerDTO
from src.entities.user_ticket.exceptions import (
    ExpiredInternationalPassportError,
    InvalidInternationalPassportError,
)
from src.entities.user_ticket.user_ticket import Passenger, UserTicket
from src.entities.user_ticket.value_objects.passport import InternationalPassport
from src.entities.value_objects.entity_id import EntityId


class UserTicketFactory:
    @classmethod
    def create(cls, user_id: UUID, ticket_id: UUID, passengers_dto: list[CreatePassengerDTO]) -> UserTicket:
        passengers = []

        for passenger in passengers_dto:
            try:
                passengers.append(
                    Passenger.create(
                        gender=passenger.gender,
                        first_name=passenger.first_name,
                        second_name=passenger.second_name,
                        birth_date=passenger.birth_date,
                        passport=InternationalPassport(
                            number=passenger.passport, expiration_date=passenger.expiration_date
                        ),
                    )
                )
            except InvalidInternationalPassportError:
                raise InvalidInternationalPassportError(
                    f"{passenger.first_name} {passenger.second_name}: Неправильный номер загран паспорта - {passenger.passport}"
                )

            except ExpiredInternationalPassportError:
                raise ExpiredInternationalPassportError(
                    f"У пассажира {passenger.first_name} {passenger.second_name} истёк срок загран. паспорта"
                )

        return UserTicket.create(user_id=EntityId(user_id), ticket_id=EntityId(ticket_id), passengers=passengers)
