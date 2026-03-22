from dataclasses import dataclass


@dataclass
class Sale:
    id: int
    user_id: int
    customer_id: int | None
    sale_date: str
    total_amount: float