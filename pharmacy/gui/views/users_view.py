import tkinter as tk
from tkinter import ttk, messagebox

from repositories.user_repo import UserRepository
from services.auth_service import AuthService



class UsersView:

    def __init__(self, master, current_user):
        self.master = master
        self.current_user = current_user

        self.repo = UserRepository()
        self.auth_service = AuthService()

        self.frame = ttk.Frame(master)
        self.frame.pack(fill="both", expand=True)

        self.create_widgets()
        self.load_users()

    def create_widgets(self):

        # ==== Toolbar ====
        toolbar = ttk.Frame(self.frame)
        toolbar.pack(side="top", fill="x", padx=5, pady=5)

        ttk.Button(toolbar, text="Додати", command=self.add_user).pack(side="left", padx=5)
        ttk.Button(toolbar, text="Видалити", command=self.delete_user).pack(side="left", padx=5)

        # ==== Таблиця ====
        self.tree = ttk.Treeview(
            self.frame,
            columns=("id", "username", "role"),
            show="headings"
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("username", text="Логін")
        self.tree.heading("role", text="Роль")

        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

    def load_users(self):

        for row in self.tree.get_children():
            self.tree.delete(row)

        users = self.repo.list_all()

        for u in users:
            self.tree.insert(
                "",
                "end",
                values=(u.id, u.username, u.role_name)
            )

    def add_user(self):

        dialog = tk.Toplevel(self.frame)
        dialog.title("Новий користувач")
        dialog.geometry("350x260")

        ttk.Label(dialog, text="Логін").pack(pady=5)
        entry_username = ttk.Entry(dialog)
        entry_username.pack(pady=5)

        ttk.Label(dialog, text="Пароль").pack(pady=5)
        entry_password = ttk.Entry(dialog, show="*")
        entry_password.pack(pady=5)

        ttk.Label(dialog, text="Роль").pack(pady=5)
        combo_role = ttk.Combobox(dialog, values=["admin", "pharmacist"], state="readonly")
        combo_role.pack(pady=5)
        combo_role.current(1)

        def save():

            username = entry_username.get().strip()
            password = entry_password.get().strip()
            role_name = combo_role.get()

            if not username or not password:
                messagebox.showwarning("Помилка", "Заповніть поля")
                return

            # ⚠ Краще не хардкодити, але для простоти залишимо так
            role_id = 1 if role_name == "admin" else 2

            try:
                # 🔐 Хешування і створення робить AuthService
                self.auth_service.register(username, password, role_id)

                dialog.destroy()
                self.load_users()

            except Exception as e:
                messagebox.showerror("Помилка", str(e))

        ttk.Button(dialog, text="Зберегти", command=save).pack(pady=10)

    def delete_user(self):

        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning("Помилка", "Виберіть користувача")
            return

        item = self.tree.item(selected[0])
        user_id = item["values"][0]
        username = item["values"][1]

        if username == self.current_user.username:
            messagebox.showerror("Помилка", "Неможливо видалити самого себе")
            return

        confirm = messagebox.askyesno(
            "Підтвердження",
            f"Видалити користувача {username}?"
        )

        if confirm:
            self.repo.delete(user_id)
            self.load_users()