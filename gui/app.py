import pygubu

from gui.views.medicines_view import MedicinesView
from gui.views.categories_view import CategoriesView
from gui.views.batches_view import BatchesView
from gui.views.sales_view import SalesView
from gui.views.reports_view import ReportsView
from gui.views.users_view import UsersView
from gui.views.suppliers_view import SuppliersView
from gui.views.customers_view import CustomersView


class PharmacyApp:

    def __init__(self, current_user):

        self.current_user = current_user

        self.builder = pygubu.Builder()
        self.builder.add_from_file("gui/ui/main.ui")

        # main.ui створює tk.Tk сам
        self.root = self.builder.get_object("mainwindow")

        # ✅ Вкладки, доступні і фармацевту, і адміну
        CategoriesView(self.builder.get_object("container_categories"))
        MedicinesView(self.builder.get_object("container_medicines"))
        SuppliersView(self.builder.get_object("container_suppliers"))
        BatchesView(self.builder.get_object("container_batches"))
        CustomersView(self.builder.get_object("container_customers"))
        SalesView(
            self.builder.get_object("container_sales"),
            self.current_user
        )
        ReportsView(self.builder.get_object("container_reports"))


        # ✅ Тільки вкладка Users залежить від ролі
        self.apply_role_rules()

    def apply_role_rules(self):

        notebook = self.builder.get_object("nb_main")

        # admin: вкладку залишаємо і підключаємо UsersView
        if self.current_user.role_name == "admin":
            UsersView(self.builder.get_object("container_users"), self.current_user)
            return

        # pharmacist: прибираємо вкладку "Користувачі"
        try:
            # 1) пробуємо прибрати по "path" вкладки (якщо tab_users є реальним widget)
            tab_users_obj = self.builder.get_object("tab_users")
            tab_path = str(tab_users_obj)

            if tab_path in notebook.tabs():
                notebook.forget(tab_path)
                return

            # 2) fallback: прибираємо по назві вкладки
            for t in notebook.tabs():
                if notebook.tab(t, "text") == "Користувачі":
                    notebook.forget(t)
                    return

        except Exception:
            # якщо щось не так у UI — просто не валимось
            pass

    def run(self):
        self.root.mainloop()