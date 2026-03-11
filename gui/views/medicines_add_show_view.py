import tkinter as tk
import tkinter.messagebox as messagebox
import pygubu

from services.medicine_service import MedicineService


class MedicineForm:

    def __init__(self, master, medicine=None):

        self.result = None
        self.medicine_id = None
        self.service = MedicineService()

        # -----------------------------
        # Вікно
        # -----------------------------

        self.top = tk.Toplevel(master)
        self.top.title("Редагувати препарат" if medicine else "Додати препарат")
        self.top.geometry("350x250")
        self.top.resizable(False, False)

        # центруємо вікно
        self._center_window()

        # гарячі клавіші
        self.top.bind("<Return>", lambda e: self.on_save())
        self.top.bind("<Escape>", lambda e: self.top.destroy())

        # -----------------------------
        # UI
        # -----------------------------

        self.builder = pygubu.Builder()
        self.builder.add_from_file("gui/ui/medicine_form.ui")

        self.frame = self.builder.get_object("medicine_form", self.top)

        # поля
        self.entry_name = self.builder.get_object("entry_name")
        self.entry_manufacturer = self.builder.get_object("entry_manufacturer")
        self.entry_price = self.builder.get_object("entry_price")
        self.combo_category = self.builder.get_object("combo_category")
        self.check_prescription = self.builder.get_object("check_prescription")

        self.btn_save = self.builder.get_object("btn_save")
        self.btn_cancel = self.builder.get_object("btn_cancel")

        self.btn_cancel.configure(command=self.top.destroy)
        self.btn_save.configure(command=self.on_save)

        # -----------------------------
        # Категорії
        # -----------------------------

        self.categories = self.service.list_categories()

        self.category_map = {
            category.name: category.id
            for category in self.categories
        }

        self.combo_category["values"] = list(self.category_map.keys())

        # -----------------------------
        # Prefill (редагування)
        # -----------------------------

        if medicine:

            self.medicine_id = medicine.id

            self.entry_name.insert(0, medicine.name)

            if medicine.manufacturer:
                self.entry_manufacturer.insert(0, medicine.manufacturer)

            self.entry_price.insert(0, str(medicine.retail_price))

            if medicine.category_name:
                self.combo_category.set(medicine.category_name)

            if medicine.prescription_required:
                self.check_prescription.state(["selected"])
            else:
                self.check_prescription.state(["!selected"])

        # фокус на поле назви
        self.entry_name.focus()

    # -------------------------------------------------
    # Центрування вікна
    # -------------------------------------------------

    def _center_window(self):

        self.top.update_idletasks()

        width = self.top.winfo_width()
        height = self.top.winfo_height()

        x = (self.top.winfo_screenwidth() // 2) - (width // 2)
        y = (self.top.winfo_screenheight() // 2) - (height // 2)

        self.top.geometry(f"+{x}+{y}")

    # -------------------------------------------------
    # Збереження
    # -------------------------------------------------

    def on_save(self):

        name = self.entry_name.get().strip()
        manufacturer = self.entry_manufacturer.get().strip()
        price_text = self.entry_price.get().strip()
        category_name = self.combo_category.get()
        prescription = bool(self.check_prescription.instate(["selected"]))

        if not name:
            messagebox.showerror("Помилка", "Введіть назву")
            return

        if not category_name:
            messagebox.showerror("Помилка", "Оберіть категорію")
            return

        try:
            price = float(price_text)
        except ValueError:
            messagebox.showerror("Помилка", "Некоректна ціна")
            return

        if price < 0:
            messagebox.showerror("Помилка", "Ціна не може бути від'ємною")
            return

        category_id = self.category_map.get(category_name)

        self.result = {
            "id": self.medicine_id,
            "name": name,
            "manufacturer": manufacturer if manufacturer else None,
            "category_id": category_id,
            "price": price,
            "prescription_required": prescription
        }

        self.top.destroy()

    # -------------------------------------------------
    # Показ форми
    # -------------------------------------------------

    def show(self):

        self.top.grab_set()
        self.top.wait_window()

        return self.result