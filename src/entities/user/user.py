from dataclasses import dataclass


@dataclass
class User:
    id: int
    first_name: str
    second_name: str
    email: str
    hash_password: str
    is_superuser: bool
    is_active: bool
