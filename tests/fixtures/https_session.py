import httpx
import pytest


@pytest.fixture
async def session():
    async with httpx.AsyncClient() as session:
        yield session
