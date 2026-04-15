import pygubu
from services.medicine_service import MedicineService
from gui.views.medicines_add_show_view import MedicineForm
import tkinter.messagebox as messagebox
from utils import resource_path


class MedicinesView:

    def __init__(self, parent):

        self.service = MedicineService()

        # Завантажуємо UI
        self.builder = pygubu.Builder()
        self.builder.add_from_file(resource_path("gui/ui/medicines.ui"))

        self.root = self.builder.get_object("medicines_root", parent)

        # Отримуємо елементи
        self.tree = self.builder.get_object("tree_medicines")
        self.btn_add = self.builder.get_object("btn_add")
        self.btn_edit = self.builder.get_object("btn_edit")
        self.btn_delete = self.builder.get_object("btn_delete")

        # Підключаємо callbacks
        self.btn_add.configure(command=self.on_add)
        self.btn_edit.configure(command=self.on_edit)
        self.btn_delete.configure(command=self.on_delete)

        # Налаштовуємо таблицю
        self.setup_tree()
        self.refresh()

    # -------------------------------------------------

    def setup_tree(self):

        self.tree["columns"] = (
            "id",
            "name",
            "manufacturer",
            "category",
            "prescription_required",
            "price"
        )

        self.tree["show"] = "headings"

        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Назва")
        self.tree.heading("manufacturer", text="Виробник")
        self.tree.heading("category", text="Категорія")
        self.tree.heading("prescription_required", text="За рецептом")
        self.tree.heading("price", text="Ціна")

        self.tree.column("id", width=60, anchor="center")
        self.tree.column("name", width=220)
        self.tree.column("manufacturer", width=180)
        self.tree.column("category", width=180)
        self.tree.column("prescription_required", width=120, anchor="center")
        self.tree.column("price", width=100, anchor="center")

    # -------------------------------------------------

    def refresh(self):

        for row in self.tree.get_children():
            self.tree.delete(row)

        medicines = self.service.list_medicines()

        for med in medicines:
            self.tree.insert("", "end", values=(
                med.id,
                med.name,
                med.manufacturer or "",
                med.category_name or "",
                "Так" if med.prescription_required else "Ні",
                med.retail_price
            ))

    # -------------------------------------------------

    def on_add(self):

        form = MedicineForm(self.root)
        data = form.show()

        if not data:
            return

        self.service.create_medicine(
            name=data["name"],
            manufacturer=data["manufacturer"],
            category_id=data["category_id"],
            prescription_required=data["prescription_required"],
            retail_price=data["price"]
        )

        self.refresh()

    # -------------------------------------------------

    def on_edit(self):

        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning("Увага", "Оберіть препарат")
            return

        item = self.tree.item(selected[0])
        med_id = item["values"][0]

        medicine = self.service.get_medicine_by_id(med_id)

        if not medicine:
            messagebox.showerror("Помилка", "Препарат не знайдено")
            return

        form = MedicineForm(self.root, medicine)
        data = form.show()

        if not data:
            return

        self.service.update_medicine(
            med_id=data["id"],
            name=data["name"],
            manufacturer=data["manufacturer"],
            category_id=data["category_id"],
            prescription_required=data["prescription_required"],
            retail_price=data["price"]
        )

        self.refresh()

    # -------------------------------------------------

    def on_delete(self):

        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning("Увага", "Оберіть препарат")
            return

        item = self.tree.item(selected[0])
        med_id = item["values"][0]

        confirm = messagebox.askyesno(
            "Підтвердження",
            "Ви впевнені, що хочете видалити цей препарат?"
        )

        if not confirm:
            return

        self.service.delete_medicine(med_id)
        self.refresh()