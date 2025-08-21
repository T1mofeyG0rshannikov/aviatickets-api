from dependency_injector import containers, providers

from src.infrastructure.db.database import db_generator
from src.infrastructure.repositories.airport_repository import AirportRepository
from src.infrastructure.repositories.user_repository import UserRepository


class ReposContainer(containers.Container):
    db = providers.Resource(db_generator)
    airports_repository = providers.Factory(AirportRepository, db=db)
    user_repository = providers.Factory(UserRepository, db=db)
