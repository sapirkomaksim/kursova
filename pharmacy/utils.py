import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # тимчасова папка PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)