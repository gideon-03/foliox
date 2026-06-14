import os
import flet as ft
from main import main

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    ft.app(
        target=main,
        view=ft.AppView.WEB_BROWSER,
        host='0.0.0.0',
        port=port,
        assets_dir='assets',
    )
