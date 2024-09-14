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


class CreateArticle(ft.Container):
    def __init__(self, page, author_name, author_dict, *args, **kwargs):
        super().__init__(*args, **kwargs)

        suggested_topics = ["topic1", "topic2", "topic1"]
        self.topics_column = ft.Column(
            [],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        for topic in suggested_topics:
            self.topics_column.controls.append(
                ft.ElevatedButton(
                    text=topic,
                    on_click=self.suggested_topic_clicked,
                    expand=True,
                    style=ft.ButtonStyle(
                        padding=ft.padding.symmetric(vertical=22, horizontal=35),
                        shape=ft.RoundedRectangleBorder(radius=18),
                        text_style=ft.TextStyle(size=25),
                    ),
                ),
            )

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
            on_change=self.topic_text_field_changed, max_length=500, max_lines=10
        )

        self.choose_topic = ft.ResponsiveRow(
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
                            expand=True
                        ),
                        ft.Container(
                            ft.ElevatedButton(
                                "Generate",
                                style=ft.ButtonStyle(
                                    padding=ft.padding.symmetric(
                                        vertical=25, horizontal=40
                                    ),
                                    text_style=ft.TextStyle(size=30),
                                    color="#36e4ff",
                                    side=ft.BorderSide(
                                        2, ft.colors.with_opacity(1, "#36e4ff")
                                    ),
                                ),
                                on_click=self.generate,
                            ),
                            padding=ft.padding.only(bottom=75),
                        ),
                    ],
                    col=6,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        self.content = self.choose_topic

    def suggested_topic_clicked(self, e):
        self.topic_text_field.value = e.control.text
        self.topics_column.visible = False
        self.page.update()

    def topic_text_field_changed(self, e):
        if not e.control.value:
            self.topics_column.visible = True
        else:
            self.topics_column.visible = False
        self.page.update()

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
            text = """What does a neuron look like?
            A useful analogy is to think of a neuron as a tree. A neuron has three main parts: dendrites, an axon, and a cell body or soma (see image below), which can be represented as the branches, roots and trunk of a tree, respectively. A dendrite (tree branch) is where a neuron receives input from other cells. Dendrites branch as they move towards their tips, just like tree branches do, and they even have leaf-like structures on them called spines.

            The axon (tree roots) is the output structure of the neuron; when a neuron wants to talk to another neuron, it sends an electrical message called an action potential throughout the entire axon. The soma (tree trunk) is where the nucleus lies, where the neuron’s DNA is housed, and where proteins are made to be transported throughout the axon and dendrites. 


            The tree-like structure of a neuron. Dendritic spines are small structures that receive inputs from the axons of other neurons. Bottom-right image: a segment of dendrite from which spines branch off, like leaves off a tree branch. Note the very small size (~0.001mm). (Image: Alan Woodruff ; De Roo et al / CC BY-SA 3.0 via Commons)
            There are different types of neurons, both in the brain and the spinal cord. They are generally divided according to where they orginate, where they project to and which neurotransmitters they use.

            Concepts and definitions
            Axon – The long, thin structure in which action potentials are generated; the transmitting part of the neuron. After initiation, action potentials travel down axons to cause release of neurotransmitter.

            Dendrite – The receiving part of the neuron. Dendrites receive synaptic inputs from axons, with the sum total of dendritic inputs determining whether the neuron will fire an action potential.

            Spine – The small protrusions found on dendrites that are, for many synapses, the postsynaptic contact site.

            Action potential – Brief electrical event typically generated in the axon that signals the neuron as 'active'. An action potential travels the length of the axon and causes release of neurotransmitter into the synapse. The action potential and consequent transmitter release allow the neuron to communicate with other neurons.
            """
            topic_field = ft.TextField(
                value=topic,
                text_size=28,
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
                opacity=0.85,
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
                                        topic_field,
                                        self.article_text_field,
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                padding=50,
                            ),
                        ],
                        col={"md": 10, "xl": 7},
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
            min_lines=1, max_lines=3, max_length=500
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
            new_text = "dassssssssdsaaaaaaaaaaaaaaa"
            self.article_text_field.value = new_text
            self.page.update()
            self.page.close(self.dlg)


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
        self.padding = ft.padding.only(top=65)

        author_dict = page.client_storage.get("authors")[author_name]

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

        tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[articles_tab, create_article_tab, profile_tab],
            expand=1,
            tab_alignment=ft.TabAlignment.CENTER,
            divider_height=0.0001,
            on_change=self.tab_changed,
        )

        articles_tab.content = Articles(
            page, author_name=author_name, author_dict=author_dict, tabs=tabs
        )
        profile_tab.content = Profile(
            page, author_name=author_name, author_dict=author_dict
        )
        create_article_tab.content = CreateArticle(
            page, author_name=author_name, author_dict=author_dict
        )

        self.controls = [tabs]

    def tab_changed(self, e):
        if e.control.selected_index != 1:
            self.bottom_appbar.visible = False
            self.bottom_appbar.update()
        else:
            self.bottom_appbar.visible = True
            self.bottom_appbar.update()
