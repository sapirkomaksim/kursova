import tkinter as tk
from tkinter import messagebox
import pygubu

from services.auth_service import AuthService


class LoginView:

    def __init__(self, master):
        self.master = master
        self.current_user = None
        self.auth_service = AuthService()

        # Завантажуємо UI
        self.builder = pygubu.Builder()
        self.builder.add_from_file("gui/ui/login.ui")
        self.root = self.builder.get_object("login_root", master)

        # Отримуємо віджети
        self.entry_username = self.builder.get_object("entry_username")
        self.entry_password = self.builder.get_object("entry_password")
        self.btn_login = self.builder.get_object("btn_login")

        # Прив'язуємо кнопку
        self.btn_login.config(command=self.login)

    def login(self):

        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if not username or not password:
            messagebox.showwarning("Помилка", "Заповніть всі поля")
            return

        # 🔐 Вся логіка авторизації в AuthService
        user = self.auth_service.login(username, password)

        if not user:
            messagebox.showerror("Помилка", "Невірний логін або пароль")
            return

        # Якщо успішно
        self.current_user = user
        self.master.destroy()