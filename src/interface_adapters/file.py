from dataclasses import dataclass


@dataclass
class File:
    name: str
    content: bytes
