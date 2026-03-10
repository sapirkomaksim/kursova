import tkinter as tk
from gui.app import PharmacyApp
from gui.views.login_view import LoginView


def main():

    # Вікно логіну
    login_root = tk.Tk()
    login_root.title("Вхід у систему")
    login_root.geometry("300x250")

    login_view = LoginView(login_root)
    login_root.mainloop()

    # Якщо вхід успішний — запускаємо головне вікно
    if login_view.current_user:
        app = PharmacyApp(login_view.current_user)
        app.run()


if __name__ == "__main__":
    main()