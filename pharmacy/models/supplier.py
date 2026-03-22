# models/supplier.py

from dataclasses import dataclass


@dataclass
class Supplier:
    id: int
    name: str
    phone: str | None
    address: str | None