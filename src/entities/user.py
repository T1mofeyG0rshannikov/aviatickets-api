from dataclasses import dataclass


@dataclass
class User:
    id: int
    username: str
    email: str
    hash_password: str
    is_superuser: bool
    is_active: bool
