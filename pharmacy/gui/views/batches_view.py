import tkinter as tk
from tkinter import ttk, messagebox
import pygubu

from database.connection import get_connection
from repositories.batch_repo import BatchRepository
from repositories.medicine_repo import MedicineRepository
from repositories.supplier_repo import SupplierRepository


def _is_date_yyyy_mm_dd(s: str) -> bool:
    if len(s) != 10:
        return False
    if s[4] != "-" or s[7] != "-":
        return False
    y, m, d = s[:4], s[5:7], s[8:10]
    return y.isdigit() and m.isdigit() and d.isdigit()


class BatchesView:

    def __init__(self, master):
        self.master = master

        self.repo = BatchRepository()
        self.med_repo = MedicineRepository()
        self.sup_repo = SupplierRepository()

        self.builder = pygubu.Builder()
        self.builder.add_from_file("gui/ui/batches.ui")
        self.root = self.builder.get_object("batches_root", master)

        self.tree = self.builder.get_object("tree_batches")
        self.btn_add = self.builder.get_object("btn_add")
        self.btn_edit = self.builder.get_object("btn_edit")
        self.btn_delete = self.builder.get_object("btn_delete")

        self._setup_tree()
        self._add_scrollbars()

        self.btn_add.config(command=self.add_batch)
        self.btn_edit.config(command=self.edit_batch)
        self.btn_delete.config(command=self.delete_batch)

        self.refresh()

    # -----------------------------
    # Scrollbars
    # -----------------------------

    def _add_scrollbars(self):

        parent = self.tree.master

        scroll_y = ttk.Scrollbar(parent, orient="vertical", command=self.tree.yview)
        scroll_x = ttk.Scrollbar(parent, orient="horizontal", command=self.tree.xview)

        self.tree.configure(
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")

        # прокрутка колесом миші
        self.tree.bind(
            "<MouseWheel>",
            lambda e: self.tree.yview_scroll(int(-1 * (e.delta / 120)), "units")
        )

    # -----------------------------
    # Tree setup
    # -----------------------------

    def _setup_tree(self):

        self.tree["columns"] = (
            "id", "medicine", "supplier",
            "batch", "mfg", "exp",
            "qty", "price"
        )

        self.tree["show"] = "headings"

        self.tree.heading("id", text="ID")
        self.tree.heading("medicine", text="Препарат")
        self.tree.heading("supplier", text="Постачальник")
        self.tree.heading("batch", text="№ партії")
        self.tree.heading("mfg", text="Виготовлено")
        self.tree.heading("exp", text="Придатний до")
        self.tree.heading("qty", text="К-сть")
        self.tree.heading("price", text="Закуп. ціна")

        self.tree.column("id", width=60, anchor="center", stretch=False)
        self.tree.column("medicine", width=220, stretch=True)
        self.tree.column("supplier", width=220, stretch=True)
        self.tree.column("batch", width=120)
        self.tree.column("mfg", width=110, anchor="center")
        self.tree.column("exp", width=110, anchor="center")
        self.tree.column("qty", width=80, anchor="center")
        self.tree.column("price", width=110, anchor="e")

    # -----------------------------
    # Refresh
    # -----------------------------

    def refresh(self):

        for i in self.tree.get_children():
            self.tree.delete(i)

        for b in self.repo.list_all():
            self.tree.insert(
                "",
                "end",
                values=(
                    b.id,
                    b.medicine_name or f"#{b.medicine_id}",
                    b.supplier_name or f"#{b.supplier_id}",
                    b.batch_number,
                    b.manufacture_date,
                    b.expiration_date,
                    b.quantity,
                    f"{b.purchase_price:.2f}"
                )
            )

    # -----------------------------
    # Selected row
    # -----------------------------

    def _selected(self):

        sel = self.tree.selection()

        if not sel:
            return None

        return self.tree.item(sel[0])["values"]

    # -----------------------------
    # Batch form
    # -----------------------------

    def _batch_form(self, title: str, initial=None):

        w = tk.Toplevel(self.root)
        w.title(title)
        w.geometry("520x460")

        medicines = self.med_repo.list_all()
        suppliers = self.sup_repo.list_all()

        if not medicines:
            messagebox.showwarning(
                "Увага",
                "Спочатку додайте препарати (вкладка 'Препарати')."
            )
            w.destroy()
            return None, None

        if not suppliers:
            messagebox.showwarning(
                "Увага",
                "Спочатку додайте постачальників (вкладка 'Постачальники')."
            )
            w.destroy()
            return None, None

        med_map = {f"{m.name} (id={m.id})": m.id for m in medicines}
        sup_map = {f"{s.name} (id={s.id})": s.id for s in suppliers}

        ttk.Label(w, text="Препарат").pack(pady=5)
        cb_med = ttk.Combobox(w, values=list(med_map.keys()), state="readonly")
        cb_med.pack(fill="x", padx=10)

        ttk.Label(w, text="Постачальник").pack(pady=5)
        cb_sup = ttk.Combobox(w, values=list(sup_map.keys()), state="readonly")
        cb_sup.pack(fill="x", padx=10)

        ttk.Label(w, text="Номер партії").pack(pady=5)
        e_batch = ttk.Entry(w)
        e_batch.pack(fill="x", padx=10)

        ttk.Label(w, text="Дата виготовлення (YYYY-MM-DD)").pack(pady=5)
        e_mfg = ttk.Entry(w)
        e_mfg.pack(fill="x", padx=10)

        ttk.Label(w, text="Термін придатності (YYYY-MM-DD)").pack(pady=5)
        e_exp = ttk.Entry(w)
        e_exp.pack(fill="x", padx=10)

        ttk.Label(w, text="Кількість").pack(pady=5)
        e_qty = ttk.Entry(w)
        e_qty.pack(fill="x", padx=10)

        ttk.Label(w, text="Закупівельна ціна").pack(pady=5)
        e_price = ttk.Entry(w)
        e_price.pack(fill="x", padx=10)

        if initial:

            for k, vid in med_map.items():
                if vid == int(initial["medicine_id"]):
                    cb_med.set(k)
                    break

            for k, vid in sup_map.items():
                if vid == int(initial["supplier_id"]):
                    cb_sup.set(k)
                    break

            e_batch.insert(0, initial.get("batch_number", ""))
            e_mfg.insert(0, initial.get("manufacture_date", ""))
            e_exp.insert(0, initial.get("expiration_date", ""))
            e_qty.insert(0, str(initial.get("quantity", "")))
            e_price.insert(0, str(initial.get("purchase_price", "")))

        else:
            cb_med.current(0)
            cb_sup.current(0)

        def get():

            med_key = cb_med.get()
            sup_key = cb_sup.get()

            batch_number = e_batch.get().strip()
            mfg = e_mfg.get().strip()
            exp = e_exp.get().strip()
            qty = e_qty.get().strip()
            price = e_price.get().strip()

            if not batch_number:
                raise ValueError("Номер партії обов'язковий.")

            if not _is_date_yyyy_mm_dd(mfg):
                raise ValueError(
                    "Дата виготовлення має бути у форматі YYYY-MM-DD."
                )

            if not _is_date_yyyy_mm_dd(exp):
                raise ValueError(
                    "Термін придатності має бути у форматі YYYY-MM-DD."
                )

            if not qty.isdigit():
                raise ValueError("Кількість має бути цілим числом.")

            try:
                price_f = float(price)
            except:
                raise ValueError("Закупівельна ціна має бути числом.")

            return (
                med_map[med_key],
                sup_map[sup_key],
                batch_number,
                mfg,
                exp,
                int(qty),
                float(price_f)
            )

        return w, get

    # -----------------------------
    # Add
    # -----------------------------

    def add_batch(self):

        w, get = self._batch_form("Додати партію")

        if not w:
            return

        def save():
            try:
                med_id, sup_id, batch_number, mfg, exp, qty, price = get()

                self.repo.add(
                    med_id,
                    sup_id,
                    batch_number,
                    mfg,
                    exp,
                    qty,
                    price
                )

                w.destroy()
                self.refresh()

            except Exception as e:
                messagebox.showerror("Помилка", str(e))

        ttk.Button(w, text="Зберегти", command=save).pack(pady=10)

    # -----------------------------
    # Edit
    # -----------------------------

    def edit_batch(self):

        row = self._selected()

        if not row:
            messagebox.showwarning("Помилка", "Виберіть партію")
            return

        batch_id = int(row[0])

        batch = None

        for b in self.repo.list_all():
            if b.id == batch_id:
                batch = b
                break

        if not batch:
            messagebox.showerror("Помилка", "Партію не знайдено")
            return

        initial = {
            "medicine_id": batch.medicine_id,
            "supplier_id": batch.supplier_id,
            "batch_number": batch.batch_number,
            "manufacture_date": batch.manufacture_date,
            "expiration_date": batch.expiration_date,
            "quantity": batch.quantity,
            "purchase_price": batch.purchase_price
        }

        w, get = self._batch_form(
            "Редагувати партію",
            initial=initial
        )

        if not w:
            return

        def save():
            try:
                med_id, sup_id, batch_number, mfg, exp, qty, price = get()

                self.repo.update(
                    batch_id,
                    med_id,
                    sup_id,
                    batch_number,
                    mfg,
                    exp,
                    qty,
                    price
                )

                w.destroy()
                self.refresh()

            except Exception as e:
                messagebox.showerror("Помилка", str(e))

        ttk.Button(w, text="Зберегти", command=save).pack(pady=10)

    # -----------------------------
    # Delete
    # -----------------------------

    def delete_batch(self):

        row = self._selected()

        if not row:
            messagebox.showwarning("Помилка", "Виберіть партію")
            return

        batch_id = int(row[0])

        if not messagebox.askyesno(
            "Підтвердження",
            f"Видалити партію ID={batch_id}?"
        ):
            return

        try:
            self.repo.delete(batch_id)
            self.refresh()

        except Exception as e:
            messagebox.showerror("Помилка", str(e))

    # -----------------------------
    # FEFO batches
    # -----------------------------

    def get_fefo_batches(self, medicine_id: int):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, quantity, purchase_price, expiration_date
            FROM batches
            WHERE medicine_id = ?
              AND quantity > 0
            ORDER BY expiration_date ASC
        """, (int(medicine_id),))

        rows = cur.fetchall()
        conn.close()

        return rows

    # -----------------------------
    # decrease quantity
    # -----------------------------

    def decrease_quantity(self, batch_id: int, qty: int):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE batches
            SET quantity = quantity - ?
            WHERE id = ?
        """, (int(qty), int(batch_id)))

        conn.commit()
        conn.close()