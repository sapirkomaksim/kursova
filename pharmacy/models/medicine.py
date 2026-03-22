from dataclasses import dataclass


@dataclass
class Medicine:
    id: int
    name: str
    manufacturer: str | None
    category_id: int | None
    prescription_required: bool
    retail_price: float
    category_name: str | None = None   #додали