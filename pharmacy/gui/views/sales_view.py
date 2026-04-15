import tkinter as tk
from tkinter import ttk, messagebox
import pygubu

from repositories.medicine_repo import MedicineRepository
from repositories.customer_repo import CustomerRepository
from repositories.sale_repo import SaleRepository
from services.sales_service import SalesService
from repositories.batch_repo import BatchRepository
from utils import resource_path


class SalesView:

    def __init__(self, master, current_user):

        self.master = master
        self.current_user = current_user

        self.service = SalesService()
        self.sale_repo = SaleRepository()
        self.med_repo = MedicineRepository()
        self.customer_repo = CustomerRepository()
        self.batch_repo = BatchRepository()

        self.builder = pygubu.Builder()
        self.builder.add_from_file(resource_path("gui/ui/sales.ui"))

        self.root = self.builder.get_object("sales_root", master)
        self.btn_new = self.builder.get_object("btn_new_sale")
        self.btn_refresh = self.builder.get_object("btn_refresh")
        self.tree = self.builder.get_object("tree_sales")

        self.btn_new.config(command=self.new_sale)
        self.btn_refresh.config(command=self.refresh_sales_table)

        self._setup_tree()
        self._add_scrollbars()

        self.refresh_sales_table()

    # ------------------------------------------------
    # Scrollbars
    # ------------------------------------------------

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

        self.tree.bind(
            "<MouseWheel>",
            lambda e: self.tree.yview_scroll(int(-1 * (e.delta / 120)), "units")
        )

    # ------------------------------------------------
    # Tree setup
    # ------------------------------------------------

    def _setup_tree(self):

        self.tree["columns"] = (
            "id",
            "medicine",
            "batch",
            "customer",
            "seller",
            "date",
            "exp",
            "qty",
            "price",
            "total"
        )

        self.tree["show"] = "headings"

        self.tree.heading("id", text="ID")
        self.tree.heading("medicine", text="Ліки")
        self.tree.heading("batch", text="Партія")
        self.tree.heading("customer", text="Покупець")
        self.tree.heading("seller", text="Продавець")
        self.tree.heading("date", text="Дата продажу")
        self.tree.heading("exp", text="Термін придатності")
        self.tree.heading("qty", text="Кількість")
        self.tree.heading("price", text="Ціна")
        self.tree.heading("total", text="Сума")

        self.tree.column("id", width=60, anchor="center")
        self.tree.column("medicine", width=180)
        self.tree.column("batch", width=100)
        self.tree.column("customer", width=180)
        self.tree.column("seller", width=120)
        self.tree.column("date", width=150)
        self.tree.column("exp", width=120)
        self.tree.column("qty", width=80, anchor="center")
        self.tree.column("price", width=100, anchor="e")
        self.tree.column("total", width=120, anchor="e")

    # ------------------------------------------------
    # Refresh sales
    # ------------------------------------------------

    def refresh_sales_table(self):

        for row in self.tree.get_children():
            self.tree.delete(row)

        sales = self.sale_repo.list_all()

        for s in sales:

            (
                sid,
                medicine,
                batch,
                customer,
                seller,
                date,
                exp,
                qty,
                price,
                total
            ) = s

            self.tree.insert("", "end", values=(
                sid,
                medicine,
                batch,
                customer,
                seller,
                date,
                exp,
                qty,
                price,
                total
            ))

    # ------------------------------------------------
    # New sale
    # ------------------------------------------------

    def new_sale(self):

        if not self.current_user:
            messagebox.showerror("Помилка", "Користувач не визначений.")
            return

        w = tk.Toplevel(self.root)
        w.title("Новий продаж")
        w.geometry("720x500")

        medicines = self.med_repo.list_all()
        customers = self.customer_repo.list_all()

        if not medicines:
            messagebox.showwarning("Увага", "Немає препаратів")
            w.destroy()
            return

        if not customers:
            messagebox.showwarning("Увага", "Немає покупців")
            w.destroy()
            return

        med_map = {f"{m.name} (id={m.id})": m.id for m in medicines}
        cust_map = {f"{c.full_name} (id={c.id})": c.id for c in customers}

        # --------------------------
        # Покупець
        # --------------------------

        ttk.Label(w, text="Покупець").pack(pady=5)

        cb_customer = ttk.Combobox(
            w,
            values=list(cust_map.keys()),
            state="readonly"
        )
        cb_customer.pack(fill="x", padx=10)
        cb_customer.current(0)

        # --------------------------
        # Препарат
        # --------------------------

        ttk.Label(w, text="Препарат").pack(pady=5)

        cb_medicine = ttk.Combobox(
            w,
            values=list(med_map.keys()),
            state="readonly"
        )
        cb_medicine.pack(fill="x", padx=10)
        cb_medicine.current(0)

        # --------------------------
        # Таблиця партій + scroll
        # --------------------------

        ttk.Label(w, text="Доступні партії").pack(pady=5)

        frame_batches = ttk.Frame(w)
        frame_batches.pack(fill="both", expand=True, padx=10, pady=5)

        scroll_y = ttk.Scrollbar(frame_batches, orient="vertical")
        scroll_x = ttk.Scrollbar(frame_batches, orient="horizontal")

        tree_batches = ttk.Treeview(
            frame_batches,
            columns=("batch", "exp", "qty", "price"),
            show="headings",
            height=8,
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )

        scroll_y.config(command=tree_batches.yview)
        scroll_x.config(command=tree_batches.xview)

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        tree_batches.pack(fill="both", expand=True)

        tree_batches.heading("batch", text="Партія")
        tree_batches.heading("exp", text="Термін придатності")
        tree_batches.heading("qty", text="Залишок")
        tree_batches.heading("price", text="Ціна")

        tree_batches.column("batch", width=120)
        tree_batches.column("exp", width=120)
        tree_batches.column("qty", width=80, anchor="center")
        tree_batches.column("price", width=100, anchor="e")

        # --------------------------
        # Кількість
        # --------------------------

        frame_bottom = ttk.Frame(w)
        frame_bottom.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame_bottom, text="Кількість").pack(side="left")

        e_qty = ttk.Entry(frame_bottom, width=10)
        e_qty.pack(side="left", padx=10)

        # --------------------------
        # Load batches
        # --------------------------

        def load_batches():

            tree_batches.delete(*tree_batches.get_children())

            medicine_id = med_map[cb_medicine.get()]

            batches = self.batch_repo.get_batches_by_medicine(medicine_id)

            for b in batches:

                batch_id, batch_number, exp, qty, price = b

                tree_batches.insert(
                    "",
                    "end",
                    iid=batch_id,
                    values=(batch_number, exp, qty, price)
                )

        cb_medicine.bind("<<ComboboxSelected>>", lambda e: load_batches())

        load_batches()

        # --------------------------
        # Save sale
        # --------------------------

        def save():

            try:

                selected = tree_batches.focus()

                if not selected:
                    raise Exception("Виберіть партію")

                batch_id = int(selected)

                qty_text = e_qty.get().strip()

                if not qty_text.isdigit():
                    raise Exception("Кількість повинна бути числом")

                qty = int(qty_text)

                if qty <= 0:
                    raise Exception("Кількість повинна бути > 0")

                sale_id = self.service.sell_from_batch(
                    user_id=self.current_user.id,
                    customer_id=cust_map[cb_customer.get()],
                    batch_id=batch_id,
                    qty=qty
                )

                messagebox.showinfo(
                    "Успіх",
                    f"Продаж створено (ID={sale_id})"
                )

                # 🔥 оновлення партій
                load_batches()

                # 🔥 оновлення таблиці продажів
                self.refresh_sales_table()

                w.destroy()

            except Exception as e:

                messagebox.showerror("Помилка", str(e))

        ttk.Button(
            w,
            text="Продати",
            command=save
        ).pack(pady=10)