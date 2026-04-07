# services/inventory_service.py

from repositories.batch_repo import BatchRepository
from repositories.medicine_repo import MedicineRepository


class InventoryService:

    def __init__(self):
        self.batch_repo = BatchRepository()
        self.medicine_repo = MedicineRepository()

    def add_batch(
        self,
        medicine_id: int,
        supplier_id: int,
        batch_number: str,
        manufacture_date: str,
        expiration_date: str,
        quantity: int,
        purchase_price: float
    ):
        return self.batch_repo.add(
            medicine_id,
            supplier_id,
            batch_number,
            manufacture_date,
            expiration_date,
            quantity,
            purchase_price
        )

    def get_stock(self, medicine_id: int) -> int:
        batches = self.batch_repo.get_fefo_batches(medicine_id)
        return sum(batch.quantity for batch in batches)

    def get_expired_batches(self):
        batches = self.batch_repo.get_fefo_batches(medicine_id=1)  # тимчасово
        return [b for b in batches if b.is_expired()]