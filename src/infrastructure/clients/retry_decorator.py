import asyncio
import functools
from collections.abc import Callable
from typing import Any

import httpx

from src.application.exceptions import FetchAPIError


def retry(
    exceptions: tuple[type[BaseException], ...] = (httpx.HTTPError,),
    retries: int = 2,
):
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            for attempt in range(retries + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions:
                    if attempt < retries:
                        await asyncio.sleep(1)
                    else:
                        raise FetchAPIError()
            raise FetchAPIError()

        return wrapper

    return decorator
