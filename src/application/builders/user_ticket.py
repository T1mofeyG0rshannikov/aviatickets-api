from src.application.dto.user import UserDTO
from src.application.dto.user_ticket import PassengerDTO, UserTicketFullInfoDTO
from src.application.persistence.dao.ticket_dao import TicketDAOInterface
from src.entities.tickets.exceptions import TicketNotFoundError
from src.entities.user.exceptions import UserNotFoundError
from src.entities.user.user_repository import UserRepositoryInterface
from src.entities.user_ticket.user_ticket import UserTicket


class UserTicketFullInfoAssembler:
    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        ticket_dao: TicketDAOInterface,
    ) -> None:
        self.user_repository = user_repository
        self.ticket_dao = ticket_dao

    async def execute(self, user_ticket: UserTicket) -> UserTicketFullInfoDTO:
        user = await self.user_repository.get(id=user_ticket.user_id)

        if user is None:
            raise UserNotFoundError(f"no user with id = '{user_ticket.user_id}'")

        ticket = await self.ticket_dao.get(id=user_ticket.ticket_id)

        if ticket is None:
            raise TicketNotFoundError(f"no ticket with id = '{user_ticket.ticket_id}'")

        return UserTicketFullInfoDTO(
            id=user_ticket.id.value,
            user=UserDTO.from_entity(user),
            ticket=ticket,
            passengers=[
                PassengerDTO(
                    id=passenger.id.value,
                    gender=passenger.gender,
                    first_name=passenger.first_name,
                    second_name=passenger.second_name,
                )
                for passenger in user_ticket.passengers
            ],
        )
