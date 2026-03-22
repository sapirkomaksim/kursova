from dataclasses import dataclass

@dataclass
class Customer:
    id: int
    full_name: str
    phone: str | None = None
    created_at: str | None = None