import flet as ft


class MyRadio(ft.Radio):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_style = ft.TextStyle(size=18)
        self.col = {"sm": 6, "md": 4, "xl": 3}


class MyTextField(ft.TextField):
    def __init__(self, multiline=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.border_color = ft.colors.TRANSPARENT
        self.focused_border_color = ft.colors.with_opacity(0.1, "#C2E0FF")
        self.text_size = 25
        self.border_radius = 30
        self.bgcolor = ft.colors.with_opacity(0.1, "white")
        self.content_padding = ft.padding.symmetric(horizontal=30, vertical=15)
        self.multiline = multiline


class CreateAuthorView(ft.View):
    def __init__(self, page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page
        self.scroll = "AUTO"

        # Fields
        self.name = MyTextField(label="Name", max_length=50, multiline=False)
        self.description = MyTextField(label="Description or Biography", max_length=500)
        self.keywords = MyTextField(label="Keywords or Phrases", max_length=300)
        self.articles_topic = MyTextField(label="Articles Topic", max_length=300)
        self.text_tone = ft.RadioGroup(
            content=ft.Column(
                [
                    ft.Text("Select text tone:", size=20, opacity=0.6),
                    ft.ResponsiveRow(
                        [
                            MyRadio(value="formal", label="Formal"),
                            MyRadio(value="informal", label="Informal"),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            )
        )
        self.text_style = ft.RadioGroup(
            content=ft.Column(
                [
                    ft.Text("Select text style:", size=20, opacity=0.6),
                    ft.ResponsiveRow(
                        [
                            MyRadio(value="artistic", label="Artistic"),
                            MyRadio(value="official", label="Official"),
                            MyRadio(value="business", label="Business"),
                            MyRadio(value="scientific", label="Scientific"),
                            MyRadio(value="journalistic", label="Journalistic"),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=-5,
            )
        )

        create_btn = ft.ElevatedButton(
            content=ft.Container(ft.Text(value="Create Author", size=20), padding=15),
            on_click=self.create_author,
        )

        container = ft.ResponsiveRow(
            [
                ft.Column(
                    [
                        self.name,
                        self.description,
                        self.keywords,
                        self.articles_topic,
                        self.text_tone,
                        self.text_style,
                        create_btn,
                    ],
                    spacing=4,
                    col={"md": 6},
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        self.controls = [
            ft.Container(
                content=container,
                padding=ft.padding.all(40),
            )
        ]

    def create_author(self, e):
        if self.name.value in self.page.client_storage.get("authors"):
            dlg = ft.AlertDialog(
                title=ft.Text(
                    "Author with this name already exists",
                    text_align=ft.TextAlign.CENTER,
                ),
                content=ft.ElevatedButton(
                    "Okay", on_click=lambda e: self.page.close(dlg)
                ),
            )
            self.page.open(dlg)
        elif self.name.value:
            authors_dict = self.page.client_storage.get("authors")
            authors_dict[self.name.value] = {
                "description": self.description.value,
                "keywords": self.keywords.value,
                "articles_topic": self.articles_topic.value,
                "text_tone": self.text_tone.value if self.text_tone.value else "",
                "text_style": self.text_style.value if self.text_style.value else "",
                "articles": [],
            }
            self.page.client_storage.set("authors", authors_dict)
            self.page.go("/")
        else:
            dlg = ft.AlertDialog(
                title=ft.Text("Give your author a name!"),
                content=ft.ElevatedButton(
                    "Okay", on_click=lambda e: self.page.close(dlg)
                ),
            )
            self.page.open(dlg)
