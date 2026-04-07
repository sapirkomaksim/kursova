# services/medicine_service.py

from repositories.medicine_repo import MedicineRepository
from repositories.category_repo import CategoryRepository

class MedicineService:

    def __init__(self):
        self.medicine_repo = MedicineRepository()
        self.category_repo = CategoryRepository()

    def create_medicine(self, name, manufacturer, category_id, prescription_required, retail_price):
        return self.medicine_repo.add(
            name,
            manufacturer,
            category_id,
            prescription_required,
            retail_price
        )

    def list_medicines(self):
        return self.medicine_repo.list_all()

    def change_price(self, medicine_id: int, new_price: float):
        if new_price < 0:
            raise ValueError("Ціна не може бути від'ємною")

        self.medicine_repo.update_price(medicine_id, new_price)

    def delete_medicine(self, med_id: int):
        return self.medicine_repo.delete(med_id)

    def update_medicine(
            self,
            med_id: int,
            name: str,
            manufacturer: str | None,
            category_id: int | None,
            prescription_required: bool,
            retail_price: float
    ) -> None:
        self.medicine_repo.update(
            med_id,
            name,
            manufacturer,
            category_id,
            prescription_required,
            retail_price
        )

    def get_medicine_by_id(self, med_id: int):
        return self.medicine_repo.get_by_id(med_id)

    def list_categories(self):
        return self.category_repo.list_all()