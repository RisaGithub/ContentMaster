import flet as ft
from .create_author import MyRadio, MyTextField
from data.article_generation import generate_article, generate_topics
import data.article_generation


class LoadingDiolog(ft.AlertDialog):
    def __init__(self, page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page
        self.modal = False
        self.content = ft.ProgressRing(height=225, stroke_width=10)
        self.bgcolor = ft.colors.TRANSPARENT


class ArticleControl(ft.Container):
    def __init__(self, page, author_name, article_dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page
        self.author_name = author_name
        self.on_click = self.open_article
        self.article_dict = article_dict
        self.padding = 20
        self.bgcolor = ft.colors.with_opacity(0.1, "white")
        self.border_radius = 20
        self.content = ft.Column(
            [
                ft.Text(self.article_dict["topic"], size=25, opacity=0.8),
                ft.Text(self.get_short_text(self.article_dict["text"]), size=21),
            ]
        )

    def get_short_text(self, text):
        return (text[:150] + "...") if len(text) > 300 else text

    def open_article(self, e):
        topic = self.article_dict["topic"]
        text = self.article_dict["text"]
        self.current_topic_field = ft.TextField(
            value=topic,
            text_size=26,
            opacity=0.9,
            multiline=True,
            border_color=ft.colors.TRANSPARENT,
            focused_border_color=ft.colors.with_opacity(0.1, "#C2E0FF"),
            border_radius=40,
            bgcolor=ft.colors.with_opacity(0.05, "white"),
            content_padding=ft.padding.symmetric(horizontal=45, vertical=20),
        )
        self.article_text_field = ft.TextField(
            value=text,
            text_size=24,
            text_style=ft.TextStyle(height=0.99),
            opacity=1,
            multiline=True,
            border_color=ft.colors.TRANSPARENT,
            focused_border_color=ft.colors.with_opacity(0.1, "#C2E0FF"),
            border_radius=40,
            bgcolor=ft.colors.with_opacity(0.05, "white"),
            content_padding=ft.padding.symmetric(horizontal=45, vertical=30),
        )

        def save_article(e):
            previous_authors = self.page.client_storage.get("authors")
            previous_authors[self.author_name]["articles"].remove(self.article_dict)
            self.page.client_storage.set("authors", previous_authors)
            new_article_dict = {
                "topic": self.current_topic_field.value,
                "text": self.article_text_field.value,
            }

            previous_authors = self.page.client_storage.get("authors")
            previous_authors[self.author_name]["articles"].append(new_article_dict)
            self.page.client_storage.set("authors", previous_authors)

            self.page.close(self.dlg)
            self.content = ft.Column(
                [
                    ft.Text(new_article_dict["topic"], size=25, opacity=0.8),
                    ft.Text(self.get_short_text(new_article_dict["text"]), size=21),
                ]
            )
            self.page.update()

        content = ft.Container(
            ft.Column(
                [
                    ft.Container(
                        ft.Column(
                            [
                                self.current_topic_field,
                                self.article_text_field,
                            ],
                            scroll=ft.ScrollMode.ALWAYS,
                        ),
                        margin=10,
                        height=450,
                    ),
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "Close",
                                width=160,
                                height=65,
                                style=ft.ButtonStyle(
                                    text_style=ft.TextStyle(size=25),
                                    side=ft.BorderSide(
                                        2, ft.colors.with_opacity(1, "red")
                                    ),
                                ),
                                color="red",
                                on_click=lambda _: self.page.close(self.dlg),
                            ),
                            ft.ElevatedButton(
                                "Save",
                                width=200,
                                height=75,
                                style=ft.ButtonStyle(
                                    text_style=ft.TextStyle(size=25),
                                    side=ft.BorderSide(
                                        2, ft.colors.with_opacity(1, "#00ff62")
                                    ),
                                ),
                                color="#00ff62",
                                on_click=save_article,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
            ),
            padding=20,
            width=self.page.width,
        )

        self.dlg = ft.AlertDialog(content=content)
        self.page.open(self.dlg)


class Articles(ft.Container):
    def __init__(self, page, author_name, tabs=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page
        self.tabs = tabs
        articles = self.page.client_storage.get("authors")[author_name]["articles"]
        if not articles:
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
        else:
            articles_column = ft.Column()
            for art in articles:
                articles_column.controls.append(
                    ArticleControl(self.page, author_name=author_name, article_dict=art)
                )
            content = ft.Column(
                [
                    ft.Column(
                        [ft.Container(articles_column, padding=30)],
                        height=450,
                        scroll=ft.ScrollMode.ALWAYS,
                    ),
                    ft.ElevatedButton(
                        content=ft.Container(
                            ft.Text("Create new", size=30), padding=20
                        ),
                        on_click=self.create_article,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                col={"sm": 11, "md": 10, "xl": 7},
            )
        self.content = ft.ResponsiveRow(
            [content], alignment=ft.MainAxisAlignment.CENTER
        )

    def create_article(self, e):
        self.tabs.selected_index = 1
        try:
            self.page.views[-1].bottom_appbar.visible = True
        except Exception:
            pass
        self.page.update()


class CreateArticle(ft.Container):
    def __init__(self, page, author_name, author_dict, tabs=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page
        self.author_dict = author_dict
        self.author_name = author_name
        self.tabs = tabs

        self.topic_text_field = ft.TextField(
            label="What do you want the article to be about?",
            label_style=ft.TextStyle(size=26),
            border_color=ft.colors.TRANSPARENT,
            focused_border_color=ft.colors.with_opacity(0.1, "#C2E0FF"),
            text_size=25,
            border_radius=40,
            bgcolor=ft.colors.with_opacity(0.05, "white"),
            content_padding=ft.padding.symmetric(horizontal=35, vertical=30),
            multiline=True,
            min_lines=2,
            on_change=self.topic_text_field_changed,
            max_length=500,
            max_lines=10,
        )
        self.choose_topic_view()

    def choose_topic_view(self):
        self.topics_column = self.get_topics_column()
        self.topic_text_field.value = ""

        self.content = ft.ResponsiveRow(
            [
                ft.Column(
                    [
                        ft.Column(
                            [
                                self.topic_text_field,
                                self.topics_column,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            expand=True,
                        ),
                        ft.Container(),
                    ],
                    col={"xs": 11, "sm": 11, "md": 10, "xl": 6},
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

    def get_topics_column(self):
        dlg = LoadingDiolog(self.page)
        self.page.open(dlg)
        suggested_topics = generate_topics(
            author_dict=self.page.client_storage.get("authors")[self.author_name]
        )
        self.page.close(dlg)
        topics_column = ft.Column(
            [],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        for topic in suggested_topics:
            topics_column.controls.append(
                ft.ElevatedButton(
                    text=topic,
                    on_click=self.suggested_topic_clicked,
                    expand=True,
                    style=ft.ButtonStyle(
                        padding=ft.padding.symmetric(vertical=15, horizontal=35),
                        shape=ft.RoundedRectangleBorder(radius=18),
                        text_style=ft.TextStyle(size=20),
                    ),
                ),
            )
        return topics_column

    def suggested_topic_clicked(self, e):
        self.topic_text_field.value = e.control.text
        self.topics_column.visible = False
        self.show_generate_btn_appbar()
        self.page.update()

    def show_generate_btn_appbar(self):
        generate_btn = ft.ElevatedButton(
            "Generate",
            style=ft.ButtonStyle(
                padding=ft.padding.symmetric(vertical=25, horizontal=40),
                text_style=ft.TextStyle(size=30),
                color="#36e4ff",
                side=ft.BorderSide(2, ft.colors.with_opacity(1, "#36e4ff")),
            ),
            on_click=self.generate,
        )
        self.page.views[-1].bottom_appbar = ft.BottomAppBar(
            content=ft.Container(
                ft.Row(
                    [generate_btn],
                    spacing=32,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                blur=20,
            ),
            bgcolor=ft.colors.TRANSPARENT,
            height=150,
            padding=ft.padding.only(bottom=15),
        )
        self.page.update()

    def topic_text_field_changed(self, e):
        if not e.control.value:
            self.topics_column.visible = True
        else:
            self.topics_column.visible = False
        self.show_generate_btn_appbar()

    def generate(self, e):
        if not self.topic_text_field.value:
            dlg = ft.AlertDialog(
                title=ft.Text(
                    "Choose a topic for a new article",
                    text_align=ft.TextAlign.CENTER,
                ),
                content=ft.ElevatedButton(
                    "Okay", on_click=lambda e: self.page.close(dlg)
                ),
            )
            self.page.open(dlg)
        else:
            topic = self.topic_text_field.value
            # generate article
            dlg = LoadingDiolog(self.page)
            self.page.open(dlg)
            text = generate_article(author_dict=self.author_dict, topic=topic)
            self.page.close(dlg)
            self.current_topic_field = ft.TextField(
                value=topic,
                text_size=26,
                opacity=0.9,
                multiline=True,
                border_color=ft.colors.TRANSPARENT,
                focused_border_color=ft.colors.with_opacity(0.1, "#C2E0FF"),
                border_radius=40,
                bgcolor=ft.colors.with_opacity(0.05, "white"),
                content_padding=ft.padding.symmetric(horizontal=45, vertical=20),
            )
            self.article_text_field = ft.TextField(
                value=text,
                text_size=24,
                text_style=ft.TextStyle(height=0.99),
                opacity=1,
                multiline=True,
                border_color=ft.colors.TRANSPARENT,
                focused_border_color=ft.colors.with_opacity(0.1, "#C2E0FF"),
                border_radius=40,
                bgcolor=ft.colors.with_opacity(0.05, "white"),
                content_padding=ft.padding.symmetric(horizontal=45, vertical=30),
            )

            self.content = ft.ResponsiveRow(
                [
                    ft.Column(
                        [
                            ft.Container(
                                ft.Column(
                                    [
                                        self.current_topic_field,
                                        self.article_text_field,
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                padding=50,
                            ),
                        ],
                        col={"sm": 11, "md": 10, "xl": 7},
                        scroll=ft.ScrollMode.ALWAYS,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )

            edit_btn = ft.ElevatedButton(
                content=ft.Row(
                    [ft.Icon(ft.icons.EDIT_ROUNDED, size=25), ft.Text("Edit", size=25)],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                style=ft.ButtonStyle(
                    shadow_color="#36e4ff",
                    side=ft.BorderSide(2, ft.colors.with_opacity(1, "#36e4ff")),
                ),
                width=200,
                height=75,
                color="#36e4ff",
                on_click=self.edit_btn_clicked,
            )

            save_btn = ft.ElevatedButton(
                "Save",
                width=200,
                height=75,
                style=ft.ButtonStyle(
                    text_style=ft.TextStyle(size=25),
                    side=ft.BorderSide(2, ft.colors.with_opacity(1, "#00ff62")),
                ),
                color="#00ff62",
                on_click=self.save_article,
            )

            self.page.views[-1].bottom_appbar = ft.BottomAppBar(
                content=ft.Container(
                    ft.Row(
                        [edit_btn, save_btn],
                        spacing=32,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    blur=20,
                ),
                bgcolor=ft.colors.TRANSPARENT,
                height=150,
                padding=ft.padding.only(bottom=15),
            )

            self.page.update()

    def edit_btn_clicked(self, e):
        suggested_edits = [
            "Make the article twice as big",
            "Rephrase the first paragraph",
            "I want the text to be more scientific and have more data",
        ]
        suggested_edits_column = ft.Column(
            [],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        def suggested_edit_clicked(e):
            self.edit_text_field.value = e.control.text
            self.page.update()

        for edit in suggested_edits:
            suggested_edits_column.controls.append(
                ft.ElevatedButton(
                    text=edit,
                    on_click=suggested_edit_clicked,
                    style=ft.ButtonStyle(
                        padding=ft.padding.symmetric(vertical=18, horizontal=35),
                        shape=ft.RoundedRectangleBorder(radius=18),
                        text_style=ft.TextStyle(size=25),
                    ),
                    bgcolor=ft.colors.with_opacity(0.005, "black"),
                ),
            )

        self.edit_text_field = ft.TextField(
            label="How do you want to change the article?",
            label_style=ft.TextStyle(
                size=26, color=ft.colors.with_opacity(0.5, "white")
            ),
            border_color=ft.colors.with_opacity(0.2, "white"),
            focused_border_color=ft.colors.with_opacity(0.2, "#36e4ff"),
            text_size=25,
            border_radius=40,
            bgcolor=ft.colors.with_opacity(0.1, "black"),
            content_padding=ft.padding.symmetric(horizontal=35, vertical=30),
            multiline=True,
            min_lines=1,
            max_lines=3,
            max_length=500,
        )

        content = ft.Container(
            ft.Column(
                [
                    self.edit_text_field,
                    suggested_edits_column,
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "Close",
                                width=160,
                                height=65,
                                style=ft.ButtonStyle(
                                    text_style=ft.TextStyle(size=25),
                                    side=ft.BorderSide(
                                        2, ft.colors.with_opacity(1, "red")
                                    ),
                                ),
                                color="red",
                                on_click=lambda _: self.page.close(self.dlg),
                            ),
                            ft.ElevatedButton(
                                content=ft.Row(
                                    [
                                        ft.Icon(ft.icons.EDIT_ROUNDED, size=25),
                                        ft.Text("Edit", size=25),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                style=ft.ButtonStyle(
                                    shadow_color="#36e4ff",
                                    side=ft.BorderSide(
                                        2, ft.colors.with_opacity(1, "#36e4ff")
                                    ),
                                ),
                                width=160,
                                height=65,
                                color="#36e4ff",
                                on_click=self.edit_article,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=25,
                    ),
                ],
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True,
            ),
            padding=15,
            height=535,
        )

        self.dlg = ft.AlertDialog(content=content)

        self.page.open(self.dlg)

    def edit_article(self, e):
        if not self.edit_text_field.value:
            self.page.close(self.dlg)
        else:
            # change previos text based on edit_text_field content
            dlg = LoadingDiolog(self.page)
            self.page.open(dlg)
            new_text = data.article_generation.edit_article(
                article_text=self.article_text_field.value,
                changes=self.edit_text_field.value,
            )
            self.page.close(dlg)
            self.article_text_field.value = new_text
            self.page.update()
            self.page.close(self.dlg)

    def save_article(self, e):
        article_dict = {
            "topic": self.current_topic_field.value,
            "text": self.article_text_field.value,
        }
        authors_dict = self.page.client_storage.get("authors")
        # add new article to author
        authors_dict[self.author_name]["articles"].append(article_dict)
        # save
        self.page.client_storage.set("authors", authors_dict)
        self.choose_topic_view()
        self.show_generate_btn_appbar()
        self.page.views[-1].bottom_appbar.visible = False
        self.tabs.selected_index = 0
        self.page.views[-1].tab_changed()
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
        self.page.go("/")


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
        self.author_name = author_name
        self.padding = ft.padding.only(top=65)

        author_dict = page.client_storage.get("authors")[author_name]
        self.author_dict = author_dict

        articles_tab = MyTab(
            text="Articles",
            content=ft.Container(),
        )
        create_article_tab = MyTab(
            text="New",
            icon=ft.icons.ADD_ROUNDED,
            content=ft.Container(),
        )
        profile_tab = MyTab(
            text="Profile",
            icon=ft.icons.SETTINGS,
            content=ft.Container(),
        )

        self.tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[articles_tab, create_article_tab, profile_tab],
            expand=1,
            tab_alignment=ft.TabAlignment.CENTER,
            divider_height=0.0001,
            on_change=self.tab_changed,
        )

        articles_tab.content = Articles(page, author_name=author_name, tabs=self.tabs)
        profile_tab.content = Profile(
            page, author_name=author_name, author_dict=author_dict
        )
        create_article_tab.content = CreateArticle(
            page, author_name=author_name, author_dict=author_dict, tabs=self.tabs
        )

        self.controls = [self.tabs]

    def tab_changed(self, e=None):
        if not e:
            self.tabs.tabs[0].content = Articles(
                self.page,
                author_name=self.author_name,
                tabs=self.tabs,
            )
            self.page.update()
        else:
            if e.control.selected_index != 1:
                if self.bottom_appbar:
                    self.bottom_appbar.visible = False
                    self.bottom_appbar.update()
            else:
                if self.bottom_appbar:
                    self.bottom_appbar.visible = True
                    self.bottom_appbar.update()
            if e.control.selected_index == 0:
                self.tabs.tabs[0].content = Articles(
                    self.page,
                    author_name=self.author_name,
                    tabs=self.tabs,
                )
                self.page.update()
