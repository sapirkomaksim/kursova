import tkinter as tk
from tkinter import ttk, messagebox
import pygubu

from repositories.supplier_repo import SupplierRepository

class SuppliersView:

    def __init__(self, master):
        self.master = master
        self.repo = SupplierRepository()

        self.builder = pygubu.Builder()
        self.builder.add_from_file("gui/ui/suppliers.ui")
        self.root = self.builder.get_object("suppliers_root", master)

        self.tree = self.builder.get_object("tree_suppliers")
        self.btn_add = self.builder.get_object("btn_add")
        self.btn_edit = self.builder.get_object("btn_edit")
        self.btn_delete = self.builder.get_object("btn_delete")

        self.setup_tree()
        self.btn_add.config(command=self.add_supplier)
        self.btn_edit.config(command=self.edit_supplier)
        self.btn_delete.config(command=self.delete_supplier)

        self.refresh()

    def setup_tree(self):
        self.tree["columns"] = ("id", "name", "phone", "address")
        self.tree["show"] = "headings"
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Назва")
        self.tree.heading("phone", text="Телефон")
        self.tree.heading("address", text="Адреса")

        self.tree.column("id", width=60, anchor="center")
        self.tree.column("name", width=240)
        self.tree.column("phone", width=140)
        self.tree.column("address", width=320)

    def refresh(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        for s in self.repo.list_all():
            self.tree.insert("", "end", values=(s.id, s.name, s.phone or "", s.address or ""))

    def _selected_id(self):
        sel = self.tree.selection()
        if not sel:
            return None
        vals = self.tree.item(sel[0])["values"]
        return int(vals[0])

    def _open_form(self, title, initial=None):
        w = tk.Toplevel(self.root)
        w.title(title)
        w.geometry("420x220")

        ttk.Label(w, text="Назва").pack(pady=5)
        e_name = ttk.Entry(w)
        e_name.pack(fill="x", padx=10)

        ttk.Label(w, text="Телефон").pack(pady=5)
        e_phone = ttk.Entry(w)
        e_phone.pack(fill="x", padx=10)

        ttk.Label(w, text="Адреса").pack(pady=5)
        e_addr = ttk.Entry(w)
        e_addr.pack(fill="x", padx=10)

        if initial:
            e_name.insert(0, initial[0])
            e_phone.insert(0, initial[1])
            e_addr.insert(0, initial[2])

        def get():
            return e_name.get().strip(), e_phone.get().strip() or None, e_addr.get().strip() or None

        return w, get

    def add_supplier(self):
        win, get = self._open_form("Додати постачальника")
        def save():
            name, phone, addr = get()
            if not name:
                messagebox.showwarning("Помилка", "Назва обов'язкова")
                return
            try:
                self.repo.add(name, phone, addr)
                win.destroy()
                self.refresh()
            except Exception as e:
                messagebox.showerror("Помилка", str(e))
        ttk.Button(win, text="Зберегти", command=save).pack(pady=10)

    def edit_supplier(self):
        sid = self._selected_id()
        if sid is None:
            messagebox.showwarning("Помилка", "Виберіть постачальника")
            return

        # дістаємо дані з таблиці (з виділеного рядка)
        item = self.tree.item(self.tree.selection()[0])["values"]
        initial = (item[1], item[2], item[3])

        win, get = self._open_form("Редагувати постачальника", initial=initial)
        def save():
            name, phone, addr = get()
            if not name:
                messagebox.showwarning("Помилка", "Назва обов'язкова")
                return
            try:
                self.repo.update(sid, name, phone, addr)
                win.destroy()
                self.refresh()
            except Exception as e:
                messagebox.showerror("Помилка", str(e))
        ttk.Button(win, text="Зберегти", command=save).pack(pady=10)

    def delete_supplier(self):
        sid = self._selected_id()
        if sid is None:
            messagebox.showwarning("Помилка", "Виберіть постачальника")
            return

        if not messagebox.askyesno("Підтвердження", "Видалити постачальника?"):
            return

        try:
            self.repo.delete(sid)
            self.refresh()
        except Exception as e:
            # якщо є партії з цим постачальником — FK не дасть видалити
            messagebox.showerror("Помилка", str(e))