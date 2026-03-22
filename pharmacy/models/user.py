from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    id: int
    username: str
    password_hash: str
    role_id: int
    created_at: Optional[str]
    role_name: str