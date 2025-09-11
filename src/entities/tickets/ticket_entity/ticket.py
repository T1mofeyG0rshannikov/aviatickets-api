from dataclasses import dataclass

from src.entities.tickets.ticket_entity.ticket_itinerary import TicketItinerary
from src.entities.tickets.value_objects.unique_key import TicketUniqueKey
from src.entities.value_objects.entity_id import EntityId
from src.entities.value_objects.price.price import Price


@dataclass
class Ticket:
    id: EntityId
    unique_key: TicketUniqueKey
    price: Price
    itineraries: list[TicketItinerary]

    @property
    def destination_country_id(self):
        return self.itineraries[0].segments[-1].destination_airport.country_id

    @property
    def departure_date(self):
        for segment in self.itineraries[0].segments:
            if segment.segment_number == 1:
                return segment.departure_at

    @property
    def arrival_date(self):
        for segment in self.itineraries[1].segments:
            if segment.segment_number == len(self.itineraries[1].segments):
                return segment.return_at

    @classmethod
    def create(cls, price: Price, itineraries: list[TicketItinerary]):
        return cls(
            id=EntityId.generate(),
            unique_key=TicketUniqueKey.generate(itineraries),
            price=price,
            itineraries=itineraries,
        )
