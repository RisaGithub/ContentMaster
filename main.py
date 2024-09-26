import flet as ft

from views.create_author import CreateAuthorView
from views.home import HomeView
from views.author import AuthorView


def main(page: ft.Page):
    # Font
    page.fonts = {
        "Montserrat": "assets\\fonts\\Montserrat-Regular.ttf",
    }

    # Theme
    theme = ft.Theme(font_family="Montserrat")

    # Page transition (when switching between views) on all devices
    theme.page_transitions.android = ft.PageTransitionTheme.NONE
    theme.page_transitions.ios = ft.PageTransitionTheme.NONE
    theme.page_transitions.macos = ft.PageTransitionTheme.NONE
    theme.page_transitions.linux = ft.PageTransitionTheme.NONE
    theme.page_transitions.windows = ft.PageTransitionTheme.NONE
    page.theme = theme

    # Update the page
    page.update()

    # Routes
    def route_changed(e):
        # route
        route = e.route
        troute = ft.TemplateRoute(e.route)
        print(route)
        # create according view
        if route == "/":
            view = HomeView(page)
        elif route == "/create_author":
            view = CreateAuthorView(page)
        elif troute.match("/authors/:name"):
            if troute.name not in page.client_storage.get("authors"):
                dlg = ft.AlertDialog(
                    title=ft.Text(
                        "You don't have author with this name",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    content=ft.ElevatedButton(
                        "Okay", on_click=lambda e: page.close(dlg)
                    ),
                )
                page.open(dlg)
                view = page.views[-1]
            else:
                view = AuthorView(page, author_name=troute.name)
        # change view
        page.views.append(view)
        page.update()

    # Assign function to on_route_change event
    page.on_route_change = route_changed

    page.client_storage.set("authors", {})

    page.go("/")


ft.app(target=main)
