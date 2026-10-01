import reflex as rx

from app import models
from app.pages.campus import (
    admin_page,
    borrowings_page,
    browse_page,
    detail_page,
    home_page,
    login_page,
    my_items_page,
    owner_requests_page,
    profile_page,
    request_page,
    saved_page,
    signup_page,
)
from app.states.campus_state import CampusState


def index() -> rx.Component:
    return home_page()


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(
            rel="preconnect",
            href="https://fonts.gstatic.com",
            cross_origin="",
        ),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(
    request_page,
    route="/items/[item_id]/request",
    on_load=CampusState.load_request,
)
app.add_page(
    detail_page, route="/items/[item_id]", on_load=CampusState.load_item
)
app.add_page(index, route="/", on_load=CampusState.load_home)
app.add_page(browse_page, route="/browse", on_load=CampusState.load_browse)
app.add_page(saved_page, route="/saved", on_load=CampusState.load_saved)
app.add_page(
    my_items_page, route="/my-items", on_load=CampusState.load_my_items
)
app.add_page(
    borrowings_page, route="/my-borrowings", on_load=CampusState.load_borrowings
)
app.add_page(
    owner_requests_page,
    route="/requests",
    on_load=CampusState.load_owner_requests,
)
app.add_page(profile_page, route="/profile", on_load=CampusState.load_profile)
app.add_page(admin_page, route="/admin", on_load=CampusState.load_admin)
app.add_page(login_page, route="/login", on_load=CampusState.load_auth)
app.add_page(signup_page, route="/signup", on_load=CampusState.load_auth)
