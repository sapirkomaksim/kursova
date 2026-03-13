import tkinter as tk
from gui.views.login_view import LoginView
from gui.app import PharmacyApp


def launch():

    root = tk.Tk()
    root.withdraw()  # ховаємо основне вікно

    # показуємо логін як модальне
    login_window = tk.Toplevel(root)
    login_view = LoginView(login_window)

    login_window.grab_set()  # модальне
    login_window.wait_window()  # чекаємо поки закриється

    if login_view.current_user:
        root.deiconify()  # показуємо головне вікно
        app = PharmacyApp(login_view.current_user, root)
        app.run()
    else:
        root.destroy()