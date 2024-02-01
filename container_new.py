import flet as ft
from camera_controller import CameraWidget


async def main_window(page: ft.Page):
    page.padding = 0
    page.window_width = 986
    page.window_height = 768
    await page.add_async(ft.Stack(
        controls=[
            CameraWidget(0),

        ],
        expand=True
    ))
