from dataclasses import dataclass

@dataclass
class Batch:
    id: int
    medicine_id: int
    supplier_id: int
    batch_number: str
    manufacture_date: str
    expiration_date: str
    quantity: int
    purchase_price: float
    created_at: str | None = None

    # для відображення (JOIN)
    medicine_name: str | None = None
    supplier_name: str | None = None