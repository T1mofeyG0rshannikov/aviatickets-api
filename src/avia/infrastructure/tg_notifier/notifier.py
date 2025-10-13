from aiogram import Bot

from avia.application.services.error_notifier import ErrorNotifierInterface
from avia.infrastructure.tg_notifier.config import TelegramSenderConfig


class TgNotifier(ErrorNotifierInterface):
    def __init__(self, config: TelegramSenderConfig) -> None:
        self._config = config
        self._bot = Bot(token=config.token)

    async def notify(self, error_message: str) -> None:
        for user_id in self._config.users:
            await self._bot.send_message(user_id, error_message)
