import tkinter as tk
from tkinter import ttk, messagebox
import pygubu

from repositories.customer_repo import CustomerRepository
from utils import resource_path


class CustomersView:

    def __init__(self, master):
        self.master = master
        self.repo = CustomerRepository()

        self.builder = pygubu.Builder()
        self.builder.add_from_file(resource_path("gui/ui/customers.ui"))

        self.root = self.builder.get_object("customers_root", master)

        self.tree = self.builder.get_object("tree_customers")
        self.btn_add = self.builder.get_object("btn_add")
        self.btn_edit = self.builder.get_object("btn_edit")
        self.btn_delete = self.builder.get_object("btn_delete")

        self._setup_tree()

        self.btn_add.config(command=self.add_customer)
        self.btn_edit.config(command=self.edit_customer)
        self.btn_delete.config(command=self.delete_customer)

        self.refresh()

    def _setup_tree(self):
        self.tree["columns"] = ("id", "full_name", "phone", "created_at")
        self.tree["show"] = "headings"

        self.tree.heading("id", text="ID")
        self.tree.heading("full_name", text="ПІБ")
        self.tree.heading("phone", text="Телефон")
        self.tree.heading("created_at", text="Створено")

        self.tree.column("id", width=60, anchor="center")
        self.tree.column("full_name", width=260)
        self.tree.column("phone", width=160)
        self.tree.column("created_at", width=180)

    def refresh(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        for c in self.repo.list_all():
            self.tree.insert("", "end", values=(
                c.id,
                c.full_name,
                c.phone or "",
                c.created_at
            ))

    def _selected(self):
        sel = self.tree.selection()
        if not sel:
            return None
        return self.tree.item(sel[0])["values"]

    def _form(self, title, initial=None):
        w = tk.Toplevel(self.root)
        w.title(title)
        w.geometry("400x200")

        ttk.Label(w, text="ПІБ").pack(pady=5)
        e_name = ttk.Entry(w)
        e_name.pack(fill="x", padx=10)

        ttk.Label(w, text="Телефон").pack(pady=5)
        e_phone = ttk.Entry(w)
        e_phone.pack(fill="x", padx=10)

        if initial:
            e_name.insert(0, initial[0])
            e_phone.insert(0, initial[1] or "")

        def get():
            name = e_name.get().strip()
            phone = e_phone.get().strip() or None

            if not name:
                raise ValueError("ПІБ обов'язкове")

            return name, phone

        return w, get

    def add_customer(self):
        w, get = self._form("Додати покупця")

        def save():
            try:
                name, phone = get()
                self.repo.add(name, phone)
                w.destroy()
                self.refresh()
            except Exception as e:
                messagebox.showerror("Помилка", str(e))

        ttk.Button(w, text="Зберегти", command=save).pack(pady=10)

    def edit_customer(self):
        row = self._selected()
        if not row:
            messagebox.showwarning("Помилка", "Виберіть покупця")
            return

        cid = int(row[0])
        initial = (row[1], row[2])

        w, get = self._form("Редагувати покупця", initial)

        def save():
            try:
                name, phone = get()
                self.repo.update(cid, name, phone)
                w.destroy()
                self.refresh()
            except Exception as e:
                messagebox.showerror("Помилка", str(e))

        ttk.Button(w, text="Зберегти", command=save).pack(pady=10)

    def delete_customer(self):
        row = self._selected()
        if not row:
            messagebox.showwarning("Помилка", "Виберіть покупця")
            return

        cid = int(row[0])

        if not messagebox.askyesno("Підтвердження", f"Видалити '{row[1]}'?"):
            return

        try:
            self.repo.delete(cid)
            self.refresh()
        except Exception as e:
            messagebox.showerror("Помилка", str(e))