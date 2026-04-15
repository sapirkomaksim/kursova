import pygubu
import tkinter.messagebox as messagebox
import tkinter.simpledialog as simpledialog
from services.medicine_service import MedicineService
from utils import resource_path


class CategoriesView:

    def __init__(self, parent):

        self.service = MedicineService()

        self.builder = pygubu.Builder()
        self.builder.add_from_file(resource_path("gui/ui/categories.ui"))

        # вставляємо root вкладки у контейнер notebook
        self.root = self.builder.get_object("categories_root", parent)

        # використовуємо grid (бо .ui через grid)
        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
        self.root.grid(row=0, column=0, sticky="nsew")

        # отримуємо віджети
        self.tree = self.builder.get_object("tree_categories")
        self.btn_add = self.builder.get_object("btn_add_category")
        self.btn_delete = self.builder.get_object("btn_delete_category")

        # callbacks
        self.btn_add.configure(command=self.on_add)
        self.btn_delete.configure(command=self.on_delete)

        self.setup_tree()

        # авто-ресайз колонок
        self.tree.bind("<Configure>", self._resize_columns)

        self.refresh()

    # ----------------------------------------

    def setup_tree(self):

        self.tree["columns"] = ("id", "name")
        self.tree["show"] = "headings"

        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Назва")

        # ID — фіксована
        self.tree.column("id", width=80, anchor="center", stretch=False)

        # Назва — розтягується
        self.tree.column("name", anchor="w", stretch=True)

    # ----------------------------------------

    def _resize_columns(self, event):
        """
        Автоматично розтягує колонку 'name'
        щоб вона займала весь доступний простір.
        """
        total_width = event.width
        id_width = 80
        new_width = max(100, total_width - id_width)
        self.tree.column("name", width=new_width)

    # ----------------------------------------

    def refresh(self):

        for row in self.tree.get_children():
            self.tree.delete(row)

        categories = self.service.list_categories()

        for category in categories:
            self.tree.insert("", "end", values=(category.id, category.name))

    # ----------------------------------------

    def on_add(self):

        name = simpledialog.askstring("Нова категорія", "Введіть назву:")

        if not name:
            return

        try:
            self.service.category_repo.add(name)
            self.refresh()
        except Exception as e:
            messagebox.showerror("Помилка", str(e))

    # ----------------------------------------

    def on_delete(self):

        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning("Увага", "Оберіть категорію")
            return

        item = self.tree.item(selected[0])
        category_id = item["values"][0]

        if self.service.category_repo.is_used(category_id):
            messagebox.showerror(
                "Помилка",
                "Категорія використовується у препаратах"
            )
            return

        confirm = messagebox.askyesno(
            "Підтвердження",
            "Ви впевнені, що хочете видалити категорію?"
        )
        if not confirm:
            return

        self.service.category_repo.delete(category_id)
        self.refresh()