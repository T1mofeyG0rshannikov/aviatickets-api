from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from src.entities.user_ticket.dto import CreatePassengerDTO
from src.entities.user_ticket.user_ticket import Passenger, UserTicket
from src.infrastructure.db.mappers.passengers import from_orm_to_passenger
from src.infrastructure.db.mappers.user_ticket import from_orm_to_user_ticket
from src.infrastructure.db.models.models import PassengerOrm, UserTicketOrm
from src.infrastructure.repositories.base_repository import BaseRepository


class UserTicketRepository(BaseRepository):
    async def get(self, id: int) -> UserTicket:
        result = await self.db.execute(select(UserTicketOrm).where(UserTicketOrm.id == id))

        user_ticket = result.scalar()
        return from_orm_to_user_ticket(user_ticket) if user_ticket else None

    async def get_passangers(self, user_ticket_id: int) -> list[Passenger]:
        results = await self.db.execute(select(PassengerOrm).where(PassengerOrm.user_ticket_id == user_ticket_id))

        passengers = results.scalars().all()
        return [from_orm_to_passenger(passenger) for passenger in passengers]

    async def create(self, user_id: int, ticket_id: int, passengers: list[CreatePassengerDTO]) -> UserTicket:
        try:
            user_ticket = UserTicketOrm(user_id=user_id, ticket_id=ticket_id)

            self.db.add(user_ticket)
            await self.db.flush()

            passangers_orm = [
                PassengerOrm(
                    user_ticket_id=user_ticket.id,
                    gender=passenger.gender,
                    first_name=passenger.first_name,
                    second_name=passenger.second_name,
                    birth_date=passenger.birth_date,
                    passport=passenger.passport,
                    expiration_date=passenger.expiration_date,
                )
                for passenger in passengers
            ]

            self.db.add_all(passangers_orm)
            await self.db.commit()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise e
