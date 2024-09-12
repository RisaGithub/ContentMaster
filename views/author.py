import flet as ft
from .create_author import MyRadio, MyTextField


class Articles(ft.Container):
    def __init__(self, page, author_name, author_dict, tabs=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tabs = tabs
        if not author_dict["articles"]:
            content = ft.Column(
                [
                    ft.Text("You don't have any articles yet", size=30, opacity=0.6),
                    ft.ElevatedButton(
                        content=ft.Container(ft.Text("Create", size=35), padding=25),
                        on_click=self.create_article,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        self.content = content

    def create_article(self, e):
        self.tabs.selected_index = 1
        self.page.update()


class Profile(ft.Column):
    def __init__(self, page, author_name, author_dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page
        self.scroll = "AUTO"
        self.author_name = author_name

        # Fields
        self.name = MyTextField(
            value=author_name, label="Name", max_length=50, multiline=False
        )
        self.description = MyTextField(
            value=author_dict["description"],
            label="Description or Biography",
            max_length=500,
        )
        self.keywords = MyTextField(
            value=author_dict["keywords"], label="Keywords or Phrases", max_length=300
        )
        self.articles_topic = MyTextField(
            value=author_dict["articles_topic"], label="Articles Topic", max_length=300
        )
        self.text_tone = ft.RadioGroup(
            content=ft.Column(
                [
                    ft.Text("Select text tone:", size=20),
                    ft.ResponsiveRow(
                        [
                            MyRadio(value="formal", label="Formal"),
                            MyRadio(value="informal", label="Informal"),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            value=author_dict["text_tone"],
        )
        self.text_style = ft.RadioGroup(
            content=ft.Column(
                [
                    ft.Text("Select text style:", size=20),
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
            ),
            value=author_dict["text_style"],
        )

        save_btn = ft.ElevatedButton(
            content=ft.Container(ft.Text(value="Save Changes", size=20), padding=15),
            on_click=self.save_changes,
        )
        delete_btn = ft.ElevatedButton(
            content=ft.Container(ft.Text(value="Delete Author", size=20), padding=15),
            on_click=self.delete_author,
            color="red",
        )

        container = ft.ResponsiveRow(
            [
                ft.Column(
                    [
                        delete_btn,
                        self.name,
                        self.description,
                        self.keywords,
                        self.articles_topic,
                        self.text_tone,
                        self.text_style,
                        save_btn,
                    ],
                    spacing=20,
                    col={"md": 6},
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        self.controls = [ft.Container(content=container, padding=ft.padding.all(40))]

    def save_changes(self, e):
        if (
            self.name.value in self.page.client_storage.get("authors")
            and self.name.value != self.author_name
        ):
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
            existing_dict = self.page.client_storage.get("authors")
            new_author_dict = {
                "description": self.description.value,
                "keywords": self.keywords.value,
                "articles_topic": self.articles_topic.value,
                "text_tone": self.text_tone.value,
                "text_style": self.text_style.value,
                "articles": existing_dict[self.author_name]["articles"],
            }
            if self.name.value != self.author_name:
                del existing_dict[self.author_name]
            existing_dict[self.name.value] = new_author_dict
            self.page.client_storage.set("authors", existing_dict)
            self.page.go("/")
        else:
            dlg = ft.AlertDialog(
                title=ft.Text("Give your author a name!"),
                content=ft.ElevatedButton(
                    "Okay", on_click=lambda e: self.page.close(dlg)
                ),
            )
            self.page.open(dlg)

    def delete_author(self, e):
        existing_dict = self.page.client_storage.get("authors")
        del existing_dict[self.author_name]
        self.page.client_storage.set("authors", existing_dict)


class MyTab(ft.Tab):
    def __init__(self, text, icon=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if icon:
            self.tab_content = ft.Row(
                [ft.Icon(icon, size=40), ft.Text(f"{text}  ", size=30)]
            )
        else:
            self.tab_content = ft.Text(f"  {text}  ", size=30)


class AuthorView(ft.View):
    def __init__(self, page, author_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page
        # self.scroll = ft.ScrollMode.AUTO
        self.padding = ft.padding.symmetric(vertical=50)

        author_dict = page.client_storage.get("authors")[author_name]
        print(author_dict)

        articles_tab = MyTab(
            text="Articles",
            content=ft.Container(),
        )
        create_article_tab = MyTab(
            text="New Article",
            icon=ft.icons.ADD_ROUNDED,
            content=ft.Container(),
        )
        profile_tab = MyTab(
            text="Profile",
            icon=ft.icons.SETTINGS,
            content=ft.Container(),
        )

        tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[articles_tab, create_article_tab, profile_tab],
            expand=1,
            tab_alignment=ft.TabAlignment.CENTER,
            divider_height=0.0001,
        )

        articles_tab.content = Articles(
            page, author_name=author_name, author_dict=author_dict, tabs=tabs
        )
        profile_tab.content = Profile(
            page, author_name=author_name, author_dict=author_dict
        )

        self.controls = [tabs]
