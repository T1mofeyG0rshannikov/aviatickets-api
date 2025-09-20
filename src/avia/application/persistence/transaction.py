from typing import Protocol


class Transaction(Protocol):
    async def commit(self) -> None:
        raise NotImplementedError

    async def flush(self) -> None:
        raise NotImplementedError
