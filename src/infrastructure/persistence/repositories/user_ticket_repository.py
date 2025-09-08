from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from src.entities.user_ticket.user_ticket import UserTicket
from src.entities.user_ticket.user_ticket_repository import (
    UserTicketRepositoryInterface,
)
from src.entities.value_objects.entity_id import EntityId
from src.infrastructure.persistence.db.models.models import PassengerOrm, UserTicketOrm
from src.infrastructure.persistence.persist_base import PersistBase
from src.infrastructure.persistence.repositories.mappers.user_ticket import (
    from_orm_to_user_ticket,
)


class UserTicketRepository(UserTicketRepositoryInterface, PersistBase):
    async def get(self, id: EntityId) -> UserTicket | None:
        result = await self.db.execute(
            select(UserTicketOrm).options(joinedload(UserTicketOrm.passengers)).where(UserTicketOrm.id == id.value)
        )

        user_ticket = result.scalar()
        return from_orm_to_user_ticket(user_ticket) if user_ticket else None

    async def save(self, user_ticket: UserTicket) -> None:
        try:
            user_ticket_orm = UserTicketOrm(
                id=user_ticket.id.value, user_id=user_ticket.user_id.value, ticket_id=user_ticket.ticket_id.value
            )

            await self.db.flush()

            passengers_orm = [
                PassengerOrm(
                    user_ticket_id=user_ticket.id.value,
                    gender=passenger.gender,
                    first_name=passenger.first_name,
                    second_name=passenger.second_name,
                    birth_date=passenger.birth_date,
                    passport=passenger.passport.number,
                    expiration_date=passenger.passport.expiration_date,
                )
                for passenger in user_ticket.passengers
            ]

            self.db.add(user_ticket_orm)
            self.db.add_all(passengers_orm)
            await self.db.commit()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise e
