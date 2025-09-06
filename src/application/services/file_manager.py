from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class File:
    name: str
    content: bytes


class FileManagerInterface(ABC):
    @abstractmethod
    def find_by_name(self, folder: str, file_name: str) -> File | None:
        ...

    @abstractmethod
    def save(self, folder: str, file: File) -> None:
        ...
