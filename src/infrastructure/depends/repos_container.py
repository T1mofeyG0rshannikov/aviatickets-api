from dependency_injector import containers, providers

from src.infrastructure.persistence.db.database import db_generator
from src.infrastructure.persistence.repositories.airport_repository import (
    AirportRepository,
)
from src.infrastructure.persistence.repositories.user_repository import UserRepository


class ReposContainer(containers.Container):
    db = providers.Resource(db_generator)
    airports_repository = providers.Factory(AirportRepository, db=db)
    user_repository = providers.Factory(UserRepository, db=db)
