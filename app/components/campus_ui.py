import reflex as rx

from app.states.campus_state import CampusState, Listing


FIELD = "w-full rounded-xl border border-[#dddcd5] bg-white px-4 py-3 text-sm text-[#182333] outline-none focus:border-[#3159d8] focus:ring-2 focus:ring-[#3159d8]/15"
BUTTON = "inline-flex items-center justify-center gap-2 rounded-xl bg-[#3159d8] px-5 py-3 text-sm font-semibold text-white transition hover:bg-[#2347bd] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#3159d8]"


def brand() -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.icon("repeat-2", class_name="h-5 w-5 text-[#3159d8]"),
            class_name="flex h-9 w-9 items-center justify-center rounded-xl bg-[#e9edff]",
        ),
        rx.el.span("campus", class_name="font-bold text-[#182333]"),
        rx.el.span("share", class_name="font-bold text-[#3159d8]"),
        href="/",
        class_name="flex items-center text-lg tracking-tight",
    )


def nav_link(label: str, icon: str, href: str) -> rx.Component:
    return rx.el.a(
        rx.icon(icon, class_name="h-4 w-4"),
        rx.el.span(label),
        href=href,
        class_name="flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium text-[#526071] transition hover:bg-[#e9edff] hover:text-[#3159d8]",
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            brand(),
            class_name="flex h-20 shrink-0 items-center border-b border-[#ecebe4] px-6",
        ),
        rx.el.nav(
            rx.el.p(
                "YOUR SPACE",
                class_name="px-3 pb-2 pt-2 text-[10px] font-bold tracking-[0.16em] text-[#9aa2aa]",
            ),
            nav_link("Home", "house", "/"),
            nav_link("Browse", "search", "/browse"),
            nav_link("My Items", "package", "/my-items"),
            nav_link("My Borrowings", "handshake", "/my-borrowings"),
            nav_link("Requests", "inbox", "/requests"),
            nav_link("Saved", "bookmark", "/saved"),
            nav_link("Profile", "user-round", "/profile"),
            rx.cond(
                CampusState.student_admin,
                nav_link(
                    "Admin statistics", "chart-no-axes-combined", "/admin"
                ),
                rx.el.span(),
            ),
            class_name="flex min-h-0 flex-1 flex-col gap-1 overflow-y-auto px-4 py-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("user-round", class_name="h-4 w-4 text-[#3159d8]"),
                    class_name="rounded-full bg-[#e9edff] p-2",
                ),
                rx.el.div(
                    rx.el.p(
                        CampusState.student_name,
                        class_name="truncate text-sm font-semibold text-[#182333]",
                    ),
                    rx.el.p(
                        CampusState.student_department,
                        class_name="truncate text-xs text-[#75808b]",
                    ),
                    class_name="min-w-0 flex-1",
                ),
                class_name="flex items-center gap-3",
            ),
            rx.el.button(
                rx.icon("log-out", class_name="h-4 w-4"),
                "Sign out",
                on_click=CampusState.logout,
                class_name="mt-4 flex w-full items-center gap-2 text-left text-xs font-medium text-[#697483] hover:text-[#3159d8]",
            ),
            class_name="shrink-0 border-t border-[#ecebe4] px-6 py-5",
        ),
        class_name="hidden h-full w-60 shrink-0 flex-col border-r border-[#ecebe4] bg-[#fffefa] lg:flex",
    )


def mobile_nav() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            brand(),
            rx.el.button(
                rx.icon("log-out", class_name="h-4 w-4"),
                on_click=CampusState.logout,
                title="Sign out",
                class_name="rounded-lg p-2 text-[#526071] hover:bg-[#e9edff]",
            ),
            class_name="flex items-center justify-between px-4 py-3",
        ),
        rx.el.nav(
            nav_link("Home", "house", "/"),
            nav_link("Browse", "search", "/browse"),
            nav_link("My Items", "package", "/my-items"),
            nav_link("My Borrowings", "handshake", "/my-borrowings"),
            nav_link("Requests", "inbox", "/requests"),
            nav_link("Saved", "bookmark", "/saved"),
            nav_link("Profile", "user-round", "/profile"),
            rx.cond(
                CampusState.student_admin,
                nav_link(
                    "Admin statistics", "chart-no-axes-combined", "/admin"
                ),
                rx.el.span(),
            ),
            class_name="flex items-center gap-1 overflow-x-auto px-2 pb-2 [&>*]:shrink-0",
        ),
        class_name="shrink-0 border-b border-[#ecebe4] bg-[#fffefa] lg:hidden",
    )


def shell(content: rx.Component) -> rx.Component:
    return rx.cond(
        CampusState.logged_in,
        rx.el.div(
            sidebar(),
            rx.el.div(
                mobile_nav(),
                rx.el.main(
                    content,
                    class_name="w-full flex-1 min-w-0 overflow-y-auto px-5 py-7 sm:px-8 lg:px-10 lg:py-9",
                ),
                class_name="flex min-h-0 min-w-0 flex-1 flex-col",
            ),
            class_name="flex h-dvh w-full overflow-hidden bg-[#faf9f5] font-['Inter']",
        ),
        rx.el.main(class_name="h-dvh bg-[#faf9f5]"),
    )


def page_heading(kicker: str, title: str, subtitle: str) -> rx.Component:
    return rx.el.div(
        rx.el.p(
            kicker,
            class_name="mb-2 text-xs font-bold uppercase tracking-[0.18em] text-[#3159d8]",
        ),
        rx.el.h1(
            title,
            class_name="text-3xl font-bold tracking-tight text-[#182333] sm:text-4xl",
        ),
        rx.el.p(
            subtitle, class_name="mt-2 text-sm leading-relaxed text-[#697483]"
        ),
        class_name="mb-8",
    )


def error_note() -> rx.Component:
    return rx.cond(
        CampusState.page_error != "",
        rx.el.p(
            CampusState.page_error,
            class_name="mb-5 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-600",
        ),
        rx.el.div(),
    )


def item_art(item: Listing, large: bool = False) -> rx.Component:
    return rx.cond(
        item["image_path"] != "",
        rx.el.img(
            src=rx.get_upload_url(item["image_path"]),
            alt=item["name"],
            class_name="h-full w-full object-cover",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("package-open", class_name="h-9 w-9 text-[#3159d8]"),
                class_name="flex h-16 w-16 items-center justify-center rounded-2xl border border-[#d6ddf5] bg-white/75",
            ),
            rx.el.p(
                item["category"],
                class_name="mt-3 text-xs font-semibold uppercase tracking-[0.16em] text-[#3159d8]",
            ),
            class_name="flex h-full w-full flex-col items-center justify-center bg-[#e9edfa]",
        ),
    )


def item_card(item: Listing) -> rx.Component:
    return rx.el.article(
        rx.el.a(
            item_art(item),
            href=f"/items/{item['id']}",
            class_name="block h-40 overflow-hidden rounded-t-2xl",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    rx.cond(item["available"], "Available", "Unavailable"),
                    class_name=rx.cond(
                        item["available"],
                        "w-fit rounded-full bg-[#e9f7c5] px-2.5 py-1 text-[11px] font-bold text-[#344915]",
                        "w-fit rounded-full bg-[#efeeea] px-2.5 py-1 text-[11px] font-bold text-[#697483]",
                    ),
                ),
                rx.cond(
                    ~item["own"],
                    rx.el.button(
                        rx.cond(
                            item["saved"],
                            rx.icon("bookmark-check", class_name="h-4 w-4"),
                            rx.icon("bookmark", class_name="h-4 w-4"),
                        ),
                        title=rx.cond(
                            item["saved"], "Remove from saved", "Save item"
                        ),
                        on_click=lambda: CampusState.toggle_saved(item["id"]),
                        class_name="rounded-lg p-1.5 text-[#3159d8] hover:bg-[#e9edff]",
                    ),
                    rx.el.span(),
                ),
                class_name="flex items-center justify-between",
            ),
            rx.el.a(
                item["name"],
                href=f"/items/{item['id']}",
                class_name="mt-3 block line-clamp-1 text-base font-semibold text-[#182333] hover:text-[#3159d8]",
            ),
            rx.el.p(
                item["description"],
                class_name="mt-1 line-clamp-2 min-h-10 text-xs leading-relaxed text-[#697483]",
            ),
            rx.el.div(
                rx.icon("map-pin", class_name="h-3.5 w-3.5"),
                rx.el.span(item["pickup_location"], class_name="truncate"),
                class_name="mt-3 flex items-center gap-1 text-xs text-[#697483]",
            ),
            rx.el.div(
                rx.el.span(
                    f"By {item['owner']}",
                    class_name="truncate text-xs text-[#697483]",
                ),
                rx.el.a(
                    rx.cond(
                        item["available"] & ~item["own"],
                        "Request to borrow →",
                        "View details →",
                    ),
                    href=rx.cond(
                        item["available"] & ~item["own"],
                        f"/items/{item['id']}/request",
                        f"/items/{item['id']}",
                    ),
                    class_name="shrink-0 text-xs font-semibold text-[#3159d8] hover:underline",
                ),
                class_name="mt-4 flex items-center justify-between gap-2 border-t border-[#efeee9] pt-3",
            ),
            class_name="p-4",
        ),
        class_name="min-w-0 overflow-hidden rounded-2xl border border-[#e6e5dd] bg-white transition-colors hover:border-[#bcc8fa]",
    )


def item_grid(items: rx.Var[list[Listing]], empty: str) -> rx.Component:
    return rx.cond(
        items.length() > 0,
        rx.el.div(
            rx.foreach(items, item_card),
            class_name="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4",
        ),
        rx.el.div(
            rx.icon(
                "package-search",
                class_name="mx-auto mb-3 h-8 w-8 text-[#3159d8]",
            ),
            rx.el.p(empty, class_name="text-sm text-[#697483]"),
            class_name="rounded-2xl border border-dashed border-[#d8d9d5] bg-white px-6 py-12 text-center",
        ),
    )


def section_heading(title: str, subtitle: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(title, class_name="text-xl font-bold text-[#182333]"),
            rx.el.p(subtitle, class_name="mt-1 text-sm text-[#75808b]"),
        ),
        rx.el.a(
            "View all",
            href="/browse",
            class_name="text-sm font-semibold text-[#3159d8] hover:underline",
        ),
        class_name="mb-4 flex items-end justify-between gap-4",
    )


def filter_select(
    label: str,
    options: rx.Var[list[str]] | list[str],
    value: rx.Var[str],
    handler: rx.event.EventType,
) -> rx.Component:
    return rx.el.label(
        rx.el.span(
            label,
            class_name="mb-1.5 block text-xs font-semibold text-[#526071]",
        ),
        rx.el.div(
            rx.el.select(
                rx.foreach(
                    options, lambda option: rx.el.option(option, value=option)
                ),
                value=value,
                on_change=handler,
                class_name="w-full appearance-none rounded-xl border border-[#dddcd5] bg-white px-3 py-2.5 pr-8 text-sm text-[#182333] outline-none focus:border-[#3159d8]",
            ),
            rx.icon(
                "chevron-down",
                class_name="pointer-events-none absolute right-3 top-3 h-4 w-4 text-[#697483]",
            ),
            class_name="relative",
        ),
        class_name="block min-w-0",
    )
