from dataclasses import dataclass
from uuid import UUID

from src.application.dto.user_ticket import UserTicketFullInfoDTO
from src.application.services.file_manager import File


@dataclass(frozen=True)
class PdfTicketRecord:
    name: str
    content_path: str
    user_ticket_id: UUID


class PdfTicket(File):
    @classmethod
    def from_user_ticket_dto(cls, user_ticket: UserTicketFullInfoDTO, content: bytes) -> "PdfTicket":
        return cls(name=cls.get_name(user_ticket), content=content)

    @classmethod
    def get_name(cls, user_ticket: UserTicketFullInfoDTO) -> str:
        first_itinerary = user_ticket.ticket.itineraries[0]
        first_segment = first_itinerary.segments[0]
        last_segment = first_itinerary.segments[-1]
        origin_airport = first_segment.origin_airport
        destination_airport = last_segment.destination_airport

        name = f"{user_ticket.user.id}-{origin_airport.city.name_english}_{origin_airport.country.name_english}-{destination_airport.city.name_english}_{destination_airport.country.name_english}.pdf"
        name = name.replace(" ", "-")

        return name
