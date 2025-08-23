from src.application.dao.ticket_dao import TicketDAOInterface
from src.application.dto.user import UserDTO
from src.application.dto.user_ticket import PassengerDTO, UserTicketFullInfoDTO
from src.entities.user.user_repository import UserRepositoryInterface
from src.entities.user_ticket.user_ticket import UserTicket
from src.entities.user_ticket.user_ticket_repository import (
    UserTicketRepositoryInterface,
)


class UserTicketFullInfoAssembler:
    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        ticket_dao: TicketDAOInterface,
        user_ticket_repository: UserTicketRepositoryInterface,
    ) -> None:
        self.user_repository = user_repository
        self.ticket_dao = ticket_dao
        self.user_ticket_repository = user_ticket_repository

    async def execute(self, user_ticket: UserTicket) -> UserTicketFullInfoDTO:
        user = await self.user_repository.get(id=user_ticket.user_id)
        ticket = await self.ticket_dao.get(id=user_ticket.ticket_id)
        passengers = await self.user_ticket_repository.get_passangers(user_ticket.id)

        return UserTicketFullInfoDTO(
            id=user_ticket.id.value,
            user=UserDTO(
                id=user.id.value,
                first_name=user.first_name,
                second_name=user.second_name,
                email=user.email,
            ),
            ticket=ticket,
            passengers=[
                PassengerDTO(
                    id=passenger.id.value,
                    gender=passenger.gender,
                    first_name=passenger.first_name,
                    second_name=passenger.second_name,
                )
                for passenger in passengers
            ],
        )
