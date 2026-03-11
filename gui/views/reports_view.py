import tkinter as tk
from tkinter import ttk
from services.report_service import ReportService


class ReportsView:

    def __init__(self, master):

        self.master = master
        self.service = ReportService()

        frame = ttk.Frame(master)
        frame.pack(fill="both", expand=True)

        # -----------------------------
        # Toolbar
        # -----------------------------

        toolbar = ttk.Frame(frame)
        toolbar.pack(fill="x")

        ttk.Button(toolbar, text="Продажі", command=self.show_sales).pack(side="left", padx=5)
        ttk.Button(toolbar, text="Залишки", command=self.show_stock).pack(side="left", padx=5)
        ttk.Button(toolbar, text="Прострочені", command=self.show_expired).pack(side="left", padx=5)
        ttk.Button(toolbar, text="Топ продажів", command=self.show_top).pack(side="left", padx=5)

        # -----------------------------
        # Таблиця + прокрутка
        # -----------------------------

        table_frame = ttk.Frame(frame)
        table_frame.pack(fill="both", expand=True)

        scroll_y = ttk.Scrollbar(table_frame, orient="vertical")
        scroll_x = ttk.Scrollbar(table_frame, orient="horizontal")

        self.tree = ttk.Treeview(
            table_frame,
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )

        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)

        # прокрутка колесом миші
        self.tree.bind(
            "<MouseWheel>",
            lambda e: self.tree.yview_scroll(int(-1 * (e.delta / 120)), "units")
        )

    # -----------------------------
    # Очистка таблиці
    # -----------------------------

    def clear_tree(self):

        for i in self.tree.get_children():
            self.tree.delete(i)

        self.tree["columns"] = ()

    # -----------------------------
    # Налаштування колонок
    # -----------------------------

    def setup_columns(self, columns, titles=None):

        self.tree["columns"] = columns

        for col in columns:

            title = titles[col] if titles and col in titles else col

            self.tree.heading(col, text=title)
            self.tree.column(
                col,
                width=150,
                anchor="center",
                stretch=True
            )

    # -----------------------------
    # Заповнення таблиці
    # -----------------------------

    def fill_table(self, data):

        for r in data:
            self.tree.insert("", "end", values=r)

    # -----------------------------
    # Продажі
    # -----------------------------

    def show_sales(self):

        self.clear_tree()

        columns = (
            "date", "medicine", "batch",
            "customer", "seller", "qty",
            "price", "total"
        )

        titles = {
            "date": "Дата",
            "medicine": "Ліки",
            "batch": "Партія",
            "customer": "Клієнт",
            "seller": "Продавець",
            "qty": "Кількість",
            "price": "Ціна",
            "total": "Сума"
        }

        self.setup_columns(columns, titles)

        data = self.service.sales()

        self.fill_table(data)

    # -----------------------------
    # Залишки
    # -----------------------------

    def show_stock(self):

        self.clear_tree()

        columns = (
            "medicine", "batch", "supplier",
            "exp", "qty", "price", "value"
        )

        titles = {
            "medicine": "Ліки",
            "batch": "Партія",
            "supplier": "Постачальник",
            "exp": "Термін",
            "qty": "Кількість",
            "price": "Ціна",
            "value": "Сума"
        }

        self.setup_columns(columns, titles)

        data = self.service.stock()

        self.fill_table(data)

    # -----------------------------
    # Прострочені
    # -----------------------------

    def show_expired(self):

        self.clear_tree()

        columns = (
            "medicine", "batch", "supplier",
            "exp", "qty"
        )

        titles = {
            "medicine": "Ліки",
            "batch": "Партія",
            "supplier": "Постачальник",
            "exp": "Термін",
            "qty": "Кількість"
        }

        self.setup_columns(columns, titles)

        data = self.service.expired()

        self.fill_table(data)

    # -----------------------------
    # Топ продажів
    # -----------------------------

    def show_top(self):

        self.clear_tree()

        columns = (
            "medicine", "qty", "total"
        )

        titles = {
            "medicine": "Ліки",
            "qty": "Продано",
            "total": "Сума"
        }

        self.setup_columns(columns, titles)

        data = self.service.top_sales()

        self.fill_table(data)