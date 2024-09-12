import flet as ft


class AuthorView(ft.View):
    def __init__(self, page, author_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page
        self.scroll = ft.ScrollMode.AUTO
        self.padding = ft.padding.symmetric(vertical=50)

        container = ft.ResponsiveRow(
            controls=[
                ft.Column(
                    [
                        ft.Text(author_name, size=50, text_align=ft.TextAlign.CENTER),
                    ],
                    col=7,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        self.controls = [container]
