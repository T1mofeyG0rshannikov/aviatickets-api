from typing import List

from sqlalchemy import select

from src.db.mappers.ticket import orm_to_ticket
from src.db.models.models import TicketOrm
from src.dto.ticket import CreateAviaTicketDTO
from src.entities.tickets.ticket import Ticket
from src.repositories.base_reposiotory import BaseRepository


class TicketRepository(BaseRepository):
    async def all(self) -> list[Ticket]:
        results = await self.db.execute(select(TicketOrm))
        tickets = results.scalars().all()
        return [orm_to_ticket(ticket) for ticket in tickets]

    async def create_many(self, tickets: list[CreateAviaTicketDTO]) -> None:
        tickets_orm = [
            TicketOrm(
                origin_airport_id=ticket.origin_airport_id,
                destination_airport_id=ticket.destination_airport_id,
                airline_id=ticket.airline_id,
                departure_at=ticket.departure_at,
                return_at=ticket.return_at,
                duration=ticket.duration,
                price=ticket.price,
                transfers=ticket.transfers,
            )
            for ticket in tickets
        ]

        self.db.add_all(tickets_orm)
        await self.db.commit()
