from abc import ABC, abstractmethod

from avia.application.usecases.user.auth.login import Login
from avia.infrastructure.depends.usecases import UsecasesDIContainer


class LoginFactoryInterface(ABC):
    @classmethod
    @abstractmethod
    async def get_login(self) -> Login:
        ...


class LoginFactory(LoginFactoryInterface):
    @classmethod
    async def get_login(self) -> Login:
        return await UsecasesDIContainer.login()
