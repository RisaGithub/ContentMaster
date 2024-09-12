import flet as ft


class AuthorIcon(ft.Container):
    def __init__(self, page, author_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page
        self.author_name = author_name

        self.on_click = self.open_author
        self.content = ft.Column(
            [
                ft.Container(
                    content=ft.Icon(ft.icons.PERSON, size=150),
                    bgcolor=ft.colors.with_opacity(0.1, "white"),
                    padding=30,
                    border_radius=30,
                ),
                ft.Text(author_name, size=22),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def open_author(self, e):
        self.page.go(f"/authors/{self.author_name}")


class HomeView(ft.View):
    def __init__(self, page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page
        self.scroll = ft.ScrollMode.AUTO
        self.controls = []

        authors = ft.ResponsiveRow(
            [],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        for author_name in page.client_storage.get("authors"):
            authors.controls.append(
                AuthorIcon(
                    page,
                    author_name=author_name,
                    col={"sm": 6, "md": 5, "lg": 3.8, "xl": 2},
                )
            )
        create_author_btn = ft.Container(
            content=ft.Icon(ft.icons.ADD_ROUNDED, size=50),
            padding=20,
            bgcolor=ft.colors.with_opacity(0.1, "white"),
            border_radius=30,
            on_click=self.create_author,
            # col={"xs": 4, "sm": 4, "md": 2.5, "lg": 2, "xl": 2, "xxl": 1.2},
        )

        famous_people = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
        )

        container = ft.ResponsiveRow(
            [
                ft.Column(
                    [
                        ft.Column(
                            [
                                ft.Text("Your Authors", size=30, opacity=0.7),
                                authors,
                                create_author_btn,
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ft.Column(
                            [
                                ft.Text("Famous People", size=30, opacity=0.7),
                                famous_people,
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                    ],
                    spacing=50,
                    col=8,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        self.controls = [
            ft.Container(container, padding=ft.padding.symmetric(vertical=70))
        ]

    def create_author(self, e):
        self.page.go("/create_author")
