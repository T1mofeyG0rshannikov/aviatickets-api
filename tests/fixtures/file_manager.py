import pytest

from avia.infrastructure.persistence.file_manager import FileManager


@pytest.fixture
def file_manager() -> FileManager:
    return FileManager()
