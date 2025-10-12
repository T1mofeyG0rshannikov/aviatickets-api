from abc import ABC, abstractmethod


class ErrorNotifierInterface(ABC):
    @abstractmethod
    async def notify(self, error_message: str) -> None:
        ...