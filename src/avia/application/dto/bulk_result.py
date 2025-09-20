from dataclasses import dataclass


@dataclass
class BulkResult:
    inserted: int
    invalid: int
    skipped: int = 0
