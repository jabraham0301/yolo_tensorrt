# Import system dependencies
import flet as ft
import os
import warnings
from container_new import main_window

warnings.filterwarnings(action='ignore', category=DeprecationWarning)
if __name__ == "__main__":
    ft.app(target=main_window)
