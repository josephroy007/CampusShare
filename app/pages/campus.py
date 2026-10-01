import reflex as rx

from app.components.campus_ui import (
    BUTTON,
    FIELD,
    brand,
    error_note,
    filter_select,
    item_art,
    item_grid,
    page_heading,
    section_heading,
    shell,
)
from app.components.listing_ui import listing_form, owner_item_row
from app.components.transaction_ui import metric, transaction_list
from app.states.campus_state import CampusState


def auth_field(
    label: str, name: str, placeholder: str, kind: str = "text"
) -> rx.Component:
    return rx.el.label(
        rx.el.span(
            label,
            class_name="mb-1.5 block text-sm font-semibold text-[#182333]",
        ),
        rx.el.input(
            name=name,
            type=kind,
            placeholder=placeholder,
            required=True,
            class_name=FIELD,
        ),
        class_name="block",
    )


def login_page() -> rx.Component:
    return rx.el.main(
        rx.el.div(brand(), class_name="mb-12"),
        rx.el.div(
            rx.el.p(
                "WELCOME BACK",
                class_name="text-xs font-bold tracking-[0.18em] text-[#3159d8]",
            ),
            rx.el.h1(
                "Your campus, shared.",
                class_name="mt-3 text-4xl font-bold tracking-tight text-[#182333]",
            ),
            rx.el.p(
                "Sign in to discover useful things right around you.",
                class_name="mt-2 text-sm text-[#697483]",
            ),
            rx.el.form(
                auth_field(
                    "Email address", "email", "you@university.edu", "email"
                ),
                auth_field("Password", "password", "Your password", "password"),
                rx.cond(
                    CampusState.auth_error != "",
                    rx.el.p(
                        CampusState.auth_error,
                        class_name="rounded-xl bg-red-50 px-4 py-3 text-sm text-red-600",
                    ),
                    rx.el.div(),
                ),
                rx.el.button(
                    "Sign in",
                    rx.icon("arrow-right", class_name="h-4 w-4"),
                    type="submit",
                    class_name=f"{BUTTON} w-full",
                ),
                on_submit=CampusState.login,
                class_name="mt-8 flex flex-col gap-5",
            ),
            rx.el.p(
                "New here? ",
                rx.el.a(
                    "Create an account",
                    href="/signup",
                    class_name="font-semibold text-[#3159d8] hover:underline",
                ),
                class_name="mt-6 text-center text-sm text-[#697483]",
            ),
            rx.el.div(
                rx.el.p(
                    "TRY THE DEMO",
                    class_name="text-[11px] font-bold tracking-[0.15em] text-[#3159d8]",
                ),
                rx.el.p(
                    "Student: maya@campusshare.demo",
                    class_name="mt-3 text-sm font-medium text-[#182333]",
                ),
                rx.el.p(
                    "Admin: alex@campusshare.demo",
                    class_name="mt-1 text-sm font-medium text-[#182333]",
                ),
                rx.el.p(
                    "Password (both): CampusDemo2026!",
                    class_name="mt-1 text-sm font-medium text-[#182333]",
                ),
                rx.el.p(
                    "Use different accounts in separate browsers to explore the shared catalog.",
                    class_name="mt-3 text-xs leading-relaxed text-[#697483]",
                ),
                class_name="mt-9 rounded-2xl border border-[#dbe3f5] bg-[#f3f5ff] p-5",
            ),
            class_name="w-full max-w-md rounded-3xl border border-[#e6e5dd] bg-white p-7 sm:p-10",
        ),
        class_name="flex min-h-dvh flex-col items-center justify-center bg-[#faf9f5] px-5 py-10 font-['Inter']",
    )


def signup_page() -> rx.Component:
    return rx.el.main(
        rx.el.div(brand(), class_name="mb-10"),
        rx.el.div(
            rx.el.p(
                "JOIN THE COMMUNITY",
                class_name="text-xs font-bold tracking-[0.18em] text-[#3159d8]",
            ),
            rx.el.h1(
                "Make more of campus.",
                class_name="mt-3 text-3xl font-bold tracking-tight text-[#182333]",
            ),
            rx.el.p(
                "Create an account to start finding and saving items.",
                class_name="mt-2 text-sm text-[#697483]",
            ),
            rx.el.form(
                auth_field("Full name", "name", "Your full name"),
                auth_field(
                    "Email address", "email", "you@university.edu", "email"
                ),
                auth_field("Department", "department", "e.g. Computer Science"),
                rx.el.label(
                    rx.el.span(
                        "Year of study",
                        class_name="mb-1.5 block text-sm font-semibold text-[#182333]",
                    ),
                    rx.el.select(
                        rx.el.option(
                            "Select your year", value="", disabled=True
                        ),
                        rx.el.option("Year 1", value="1"),
                        rx.el.option("Year 2", value="2"),
                        rx.el.option("Year 3", value="3"),
                        rx.el.option("Year 4", value="4"),
                        rx.el.option("Year 5", value="5"),
                        rx.el.option("Year 6", value="6"),
                        name="year",
                        required=True,
                        default_value="",
                        class_name=f"{FIELD} appearance-none",
                    ),
                    class_name="block",
                ),
                auth_field(
                    "Password",
                    "password",
                    "10+ characters, a letter and a number",
                    "password",
                ),
                rx.cond(
                    CampusState.auth_error != "",
                    rx.el.p(
                        CampusState.auth_error,
                        class_name="rounded-xl bg-red-50 px-4 py-3 text-sm text-red-600",
                    ),
                    rx.el.div(),
                ),
                rx.el.button(
                    "Create account",
                    type="submit",
                    class_name=f"{BUTTON} w-full",
                ),
                on_submit=CampusState.signup,
                class_name="mt-7 flex flex-col gap-4",
            ),
            rx.el.p(
                "Already have an account? ",
                rx.el.a(
                    "Sign in",
                    href="/login",
                    class_name="font-semibold text-[#3159d8] hover:underline",
                ),
                class_name="mt-6 text-center text-sm text-[#697483]",
            ),
            class_name="w-full max-w-md rounded-3xl border border-[#e6e5dd] bg-white p-7 sm:p-10",
        ),
        class_name="flex min-h-dvh flex-col items-center justify-center bg-[#faf9f5] px-5 py-10 font-['Inter']",
    )


def home_page() -> rx.Component:
    return shell(
        rx.el.div(
            error_note(),
            rx.el.section(
                rx.el.div(
                    rx.el.p(
                        "THE CAMPUS SHARING SPACE",
                        class_name="text-xs font-bold tracking-[0.18em] text-[#3159d8]",
                    ),
                    rx.el.h1(
                        "Good things are closer than you think.",
                        class_name="mt-3 max-w-xl text-3xl font-bold leading-tight tracking-tight text-[#182333] sm:text-4xl",
                    ),
                    rx.el.p(
                        "Borrow what you need from students around campus. Share what you have when you're ready.",
                        class_name="mt-3 max-w-xl text-sm leading-relaxed text-[#526071]",
                    ),
                    rx.el.form(
                        rx.el.div(
                            rx.icon(
                                "search",
                                class_name="h-5 w-5 shrink-0 text-[#697483]",
                            ),
                            rx.el.input(
                                name="search",
                                placeholder="What do you need?",
                                class_name="min-w-0 flex-1 bg-transparent text-sm text-[#182333] outline-none placeholder:text-[#939da8]",
                            ),
                            rx.el.button(
                                "Explore items",
                                type="submit",
                                class_name=BUTTON,
                            ),
                            class_name="flex w-full items-center gap-3 rounded-2xl border border-[#dcdedb] bg-white p-2 pl-4",
                        ),
                        on_submit=CampusState.search_home,
                        class_name="mt-7 w-full max-w-2xl",
                    ),
                    rx.el.a(
                        rx.icon("plus", class_name="h-4 w-4"),
                        "List an item",
                        href="/my-items",
                        class_name="mt-5 inline-flex items-center gap-2 rounded-xl border border-[#3159d8] bg-white px-5 py-3 text-sm font-semibold text-[#3159d8] hover:bg-[#e9edff]",
                    ),
                    class_name="relative z-10",
                ),
                rx.el.div(
                    rx.icon(
                        "repeat-2", class_name="h-28 w-28 text-[#3159d8]/20"
                    ),
                    class_name="absolute -right-5 -top-10 hidden h-72 w-72 items-center justify-center rounded-full border-[24px] border-[#3159d8]/5 lg:flex",
                ),
                class_name="relative overflow-hidden rounded-3xl border border-[#e3e6dd] bg-[#f1f3e7] px-6 py-10 sm:px-10",
            ),
            rx.el.section(
                rx.el.div(
                    rx.el.h2(
                        "Explore by category",
                        class_name="text-xl font-bold text-[#182333]",
                    ),
                    rx.el.p(
                        "Find your next useful thing.",
                        class_name="mt-1 text-sm text-[#75808b]",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.foreach(
                        CampusState.categories,
                        lambda category: rx.el.button(
                            rx.icon("shapes", class_name="h-4 w-4"),
                            category,
                            on_click=lambda: CampusState.choose_category(
                                category
                            ),
                            class_name=rx.cond(
                                CampusState.category == category,
                                "flex shrink-0 items-center gap-2 rounded-full border border-[#3159d8] bg-[#e9edff] px-4 py-2 text-xs font-semibold text-[#3159d8]",
                                "flex shrink-0 items-center gap-2 rounded-full border border-[#e2e2dc] bg-white px-4 py-2 text-xs font-semibold text-[#526071] hover:border-[#3159d8] hover:text-[#3159d8]",
                            ),
                        ),
                    ),
                    class_name="flex flex-wrap gap-2",
                ),
                rx.el.a(
                    "See all items →",
                    href="/browse",
                    class_name="mt-4 inline-block text-sm font-semibold text-[#3159d8] hover:underline",
                ),
                class_name="mt-10",
            ),
            rx.el.section(
                rx.el.div(
                    rx.icon("sparkles", class_name="h-5 w-5 text-[#3159d8]"),
                    rx.el.h2(
                        "Need It?",
                        class_name="text-xl font-bold text-[#182333]",
                    ),
                    class_name="flex items-center gap-2",
                ),
                rx.el.p(
                    "Describe what you're looking for in your own words. We'll find relevant available items.",
                    class_name="mt-2 text-sm text-[#697483]",
                ),
                rx.el.form(
                    rx.el.div(
                        rx.el.input(
                            name="need",
                            placeholder="e.g. I need a camera for a photography project",
                            class_name=FIELD,
                        ),
                        rx.el.button(
                            "Find matches",
                            type="submit",
                            class_name=f"{BUTTON} shrink-0",
                        ),
                        class_name="mt-4 flex flex-col gap-3 sm:flex-row",
                    ),
                    on_submit=CampusState.need_it,
                ),
                rx.cond(
                    CampusState.need_searched,
                    rx.el.div(
                        rx.cond(
                            CampusState.need_results.length() > 0,
                            item_grid(CampusState.need_results, ""),
                            rx.el.p(
                                "No matches yet. Try a different keyword or browse all available items.",
                                class_name="rounded-xl border border-[#e6e5dd] bg-white px-5 py-6 text-sm text-[#526071]",
                            ),
                        ),
                        class_name="mt-6",
                    ),
                    rx.el.div(),
                ),
                class_name="mt-10 rounded-3xl border border-[#e2e5f3] bg-[#f4f6ff] p-6 sm:p-8",
            ),
            rx.el.section(
                section_heading(
                    "Recently shared", "Fresh finds from other students."
                ),
                item_grid(
                    CampusState.home_recent,
                    "No available items yet. Check back soon.",
                ),
                class_name="mt-12",
            ),
            rx.el.section(
                section_heading(
                    "Popular picks", "Items fellow students have saved."
                ),
                item_grid(CampusState.home_popular, "No available items yet."),
                class_name="mt-12",
            ),
            rx.el.section(
                section_heading(
                    "Around your department",
                    "Available finds, with your department first.",
                ),
                item_grid(
                    CampusState.home_nearby, "No nearby available items yet."
                ),
                class_name="mt-12 pb-8",
            ),
            class_name="w-full",
        )
    )


def browse_page() -> rx.Component:
    return shell(
        rx.el.div(
            page_heading(
                "THE CATALOG",
                "Browse everything.",
                "Discover items shared by students across campus.",
            ),
            error_note(),
            rx.el.div(
                rx.icon("search", class_name="h-5 w-5 text-[#697483]"),
                rx.el.input(
                    placeholder="Search items, categories, descriptions...",
                    default_value=CampusState.search,
                    on_change=CampusState.set_search.debounce(500),
                    class_name="w-full bg-transparent text-sm text-[#182333] outline-none",
                ),
                class_name="mb-6 flex items-center gap-3 rounded-xl border border-[#dddcd5] bg-white px-4 py-3",
            ),
            rx.el.div(
                filter_select(
                    "Category",
                    CampusState.categories,
                    CampusState.category,
                    CampusState.set_category,
                ),
                filter_select(
                    "Availability",
                    ["All", "Available", "Unavailable"],
                    CampusState.availability,
                    CampusState.set_availability,
                ),
                filter_select(
                    "Condition",
                    ["All", "Like new", "Good", "Fair"],
                    CampusState.condition_filter,
                    CampusState.set_condition_filter,
                ),
                filter_select(
                    "Department",
                    CampusState.department_options,
                    CampusState.department_filter,
                    CampusState.set_department_filter,
                ),
                filter_select(
                    "Year",
                    ["All", "1", "2", "3", "4", "5", "6"],
                    CampusState.year_filter,
                    CampusState.set_year_filter,
                ),
                filter_select(
                    "Location",
                    CampusState.location_options,
                    CampusState.location_filter,
                    CampusState.set_location_filter,
                ),
                class_name="mb-8 grid grid-cols-2 gap-3 rounded-2xl border border-[#e6e5dd] bg-white p-4 md:grid-cols-3 xl:grid-cols-6",
            ),
            rx.el.div(
                rx.el.h2(
                    "Explore items",
                    class_name="text-xl font-bold text-[#182333]",
                ),
                rx.el.p(
                    f"{CampusState.listings.length()} shown",
                    class_name="text-sm text-[#697483]",
                ),
                class_name="mb-4 flex items-end justify-between",
            ),
            item_grid(
                CampusState.listings,
                "No items match these filters. Try broadening your search.",
            ),
            class_name="w-full pb-8",
        )
    )


def detail_page() -> rx.Component:
    return shell(
        rx.el.div(
            rx.el.a(
                "← Back to browse",
                href="/browse",
                class_name="mb-7 inline-block text-sm font-semibold text-[#3159d8] hover:underline",
            ),
            error_note(),
            rx.cond(
                CampusState.detail_found,
                rx.el.div(
                    rx.el.div(
                        item_art(CampusState.selected_item, True),
                        class_name="h-72 overflow-hidden rounded-2xl border border-[#e6e5dd] sm:h-96",
                    ),
                    rx.el.div(
                        rx.el.p(
                            CampusState.selected_item["category"],
                            class_name="text-xs font-bold uppercase tracking-[0.17em] text-[#3159d8]",
                        ),
                        rx.el.h1(
                            CampusState.selected_item["name"],
                            class_name="mt-2 text-3xl font-bold tracking-tight text-[#182333]",
                        ),
                        rx.el.p(
                            rx.cond(
                                CampusState.selected_item["available"],
                                "Available to borrow",
                                "Currently unavailable",
                            ),
                            class_name=rx.cond(
                                CampusState.selected_item["available"],
                                "mt-4 w-fit rounded-full bg-[#e9f7c5] px-3 py-1.5 text-xs font-bold text-[#344915]",
                                "mt-4 w-fit rounded-full bg-[#efeeea] px-3 py-1.5 text-xs font-bold text-[#697483]",
                            ),
                        ),
                        rx.cond(
                            CampusState.selected_item["available"]
                            & ~CampusState.selected_item["own"],
                            rx.el.a(
                                "Request to borrow →",
                                href=f"/items/{CampusState.selected_item['id']}/request",
                                class_name="mt-5 inline-flex rounded-xl bg-[#3159d8] px-5 py-3 text-sm font-semibold text-white hover:bg-[#2347bd]",
                            ),
                            rx.el.div(),
                        ),
                        rx.el.p(
                            CampusState.selected_item["description"],
                            class_name="mt-6 text-sm leading-7 text-[#526071]",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "CONDITION",
                                class_name="text-[11px] font-bold tracking-widest text-[#87919a]",
                            ),
                            rx.el.p(
                                CampusState.selected_item["condition"],
                                class_name="mt-1 text-sm font-semibold text-[#182333]",
                            ),
                            class_name="border-t border-[#e6e5dd] pt-4",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "PICKUP",
                                class_name="text-[11px] font-bold tracking-widest text-[#87919a]",
                            ),
                            rx.el.p(
                                CampusState.selected_item["pickup_location"],
                                class_name="mt-1 text-sm font-semibold text-[#182333]",
                            ),
                            class_name="border-t border-[#e6e5dd] pt-4",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "PREFERRED DURATION",
                                class_name="text-[11px] font-bold tracking-widest text-[#87919a]",
                            ),
                            rx.el.p(
                                f"{CampusState.selected_item['preferred_duration_days']} days",
                                class_name="mt-1 text-sm font-semibold text-[#182333]",
                            ),
                            class_name="border-t border-[#e6e5dd] pt-4",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "SHARED BY",
                                class_name="text-[11px] font-bold tracking-widest text-[#87919a]",
                            ),
                            rx.el.p(
                                f"{CampusState.selected_item['owner']} · {CampusState.selected_item['department']} · Year {CampusState.selected_item['year']}",
                                class_name="mt-1 text-sm font-semibold text-[#182333]",
                            ),
                            class_name="border-t border-[#e6e5dd] pt-4",
                        ),
                        rx.cond(
                            ~CampusState.selected_item["own"],
                            rx.el.button(
                                rx.cond(
                                    CampusState.selected_item["saved"],
                                    "Remove from saved",
                                    "Save this item",
                                ),
                                on_click=lambda: CampusState.toggle_saved(
                                    CampusState.selected_item["id"]
                                ),
                                class_name="w-fit rounded-xl border border-[#c8d2ff] bg-white px-5 py-3 text-sm font-semibold text-[#3159d8] hover:bg-[#e9edff]",
                            ),
                            rx.el.div(),
                        ),
                        rx.cond(
                            CampusState.selected_item["own"],
                            rx.el.a(
                                "Manage this listing →",
                                href="/my-items",
                                class_name="rounded-2xl border border-[#dbe3f5] bg-[#f4f6ff] p-5 text-sm font-semibold text-[#3159d8]",
                            ),
                            rx.el.div(
                                rx.el.h2(
                                    "Want to borrow this?",
                                    class_name="text-lg font-bold text-[#182333]",
                                ),
                                rx.el.p(
                                    "Choose your dates and tell the owner how you'll use it.",
                                    class_name="mt-2 text-sm leading-relaxed text-[#697483]",
                                ),
                                rx.cond(
                                    CampusState.selected_item["available"],
                                    rx.el.a(
                                        "Start a borrow request →",
                                        href=f"/items/{CampusState.selected_item['id']}/request",
                                        class_name="mt-3 inline-block text-sm font-semibold text-[#3159d8] hover:underline",
                                    ),
                                    rx.el.p(
                                        "This item is currently unavailable. Save it and check back later.",
                                        class_name="mt-3 text-sm text-[#697483]",
                                    ),
                                ),
                                class_name="rounded-2xl border border-[#dbe3f5] bg-[#f4f6ff] p-5",
                            ),
                        ),
                        class_name="flex flex-col gap-5",
                    ),
                    class_name="grid gap-8 lg:grid-cols-2",
                ),
                rx.el.div(
                    rx.icon(
                        "package-search",
                        class_name="mb-3 h-9 w-9 text-[#3159d8]",
                    ),
                    rx.el.h1(
                        "Item not found",
                        class_name="text-2xl font-bold text-[#182333]",
                    ),
                    rx.el.p(
                        "This listing may no longer be here.",
                        class_name="mt-2 text-sm text-[#697483]",
                    ),
                    rx.el.a(
                        "Browse items →",
                        href="/browse",
                        class_name="mt-4 inline-block text-sm font-semibold text-[#3159d8]",
                    ),
                    class_name="rounded-2xl border border-[#e6e5dd] bg-white p-10 text-center",
                ),
            ),
            class_name="w-full pb-8",
        )
    )


def my_items_page() -> rx.Component:
    return shell(
        rx.el.div(
            page_heading(
                "YOUR SHARED ITEMS",
                "My Items.",
                "Share useful things with your campus community.",
            ),
            error_note(),
            rx.el.div(
                rx.icon("package", class_name="h-5 w-5 text-[#3159d8]"),
                rx.el.h2(
                    "Your listings",
                    class_name="text-xl font-bold text-[#182333]",
                ),
                class_name="mb-4 flex items-center gap-2",
            ),
            rx.cond(
                CampusState.my_items.length() > 0,
                rx.el.div(
                    rx.foreach(CampusState.my_items, owner_item_row),
                    class_name="flex flex-col gap-3",
                ),
                rx.el.div(
                    rx.icon(
                        "package-open",
                        class_name="mx-auto mb-3 h-8 w-8 text-[#3159d8]",
                    ),
                    rx.el.p(
                        "No items listed yet. Start with something a classmate could use!",
                        class_name="text-sm text-[#697483]",
                    ),
                    class_name="rounded-2xl border border-dashed border-[#d8d9d5] bg-white px-6 py-12 text-center",
                ),
            ),
            rx.el.div(listing_form(), id="listing-form", class_name="mt-10"),
            class_name="w-full pb-8",
        )
    )


def request_page() -> rx.Component:
    return shell(
        rx.el.div(
            rx.el.a(
                "← Back to item",
                href=f"/items/{CampusState.selected_item['id']}",
                class_name="mb-7 inline-block text-sm font-semibold text-[#3159d8] hover:underline",
            ),
            page_heading(
                "BORROW FROM YOUR COMMUNITY",
                "Request to borrow.",
                "Send the owner your plans and preferred dates.",
            ),
            error_note(),
            rx.cond(
                CampusState.detail_found,
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            item_art(CampusState.selected_item),
                            class_name="h-44 w-full overflow-hidden rounded-2xl sm:w-48 sm:shrink-0",
                        ),
                        rx.el.div(
                            rx.el.p(
                                CampusState.selected_item["category"],
                                class_name="text-xs font-bold uppercase tracking-wider text-[#3159d8]",
                            ),
                            rx.el.h2(
                                CampusState.selected_item["name"],
                                class_name="mt-2 text-xl font-bold text-[#182333]",
                            ),
                            rx.el.p(
                                f"Shared by {CampusState.selected_item['owner']}",
                                class_name="mt-2 text-sm text-[#526071]",
                            ),
                            rx.el.p(
                                f"Pickup: {CampusState.selected_item['pickup_location']} · Up to {CampusState.selected_item['preferred_duration_days']} days",
                                class_name="mt-2 text-sm text-[#697483]",
                            ),
                        ),
                        class_name="flex flex-col gap-5 sm:flex-row",
                    ),
                    class_name="rounded-2xl border border-[#e6e5dd] bg-white p-5",
                ),
                rx.el.div(
                    "This item could not be found.",
                    class_name="rounded-2xl border border-[#e6e5dd] bg-white p-8 text-sm text-[#526071]",
                ),
            ),
            rx.cond(
                CampusState.detail_found,
                rx.cond(
                    CampusState.request_sent,
                    rx.el.div(
                        rx.icon(
                            "circle-check",
                            class_name="h-10 w-10 text-green-500",
                        ),
                        rx.el.h2(
                            "Request sent!",
                            class_name="mt-4 text-2xl font-bold text-[#182333]",
                        ),
                        rx.el.p(
                            "Your request is pending. The owner will review your dates and get back to you. Track its progress in My Borrowings.",
                            class_name="mt-2 text-sm leading-6 text-[#526071]",
                        ),
                        rx.el.a(
                            "My Borrowings →",
                            href="/my-borrowings",
                            class_name="mt-5 inline-flex text-sm font-semibold text-[#3159d8] hover:underline",
                        ),
                        class_name="mt-5 rounded-2xl border border-[#cce79b] bg-[#f4fae9] p-7",
                    ),
                    rx.cond(
                        CampusState.selected_item["own"]
                        | ~CampusState.selected_item["available"],
                        rx.el.div(
                            "You cannot request your own item or an unavailable item. Browse for another listing.",
                            class_name="mt-5 rounded-2xl border border-[#e6e5dd] bg-white p-6 text-sm text-[#526071]",
                        ),
                        rx.el.div(
                            rx.el.h2(
                                "Plan your borrow",
                                class_name="text-xl font-bold text-[#182333]",
                            ),
                            rx.el.p(
                                "Dates include both pickup and return days. Please stay within the owner's preferred duration.",
                                class_name="mt-2 text-sm text-[#697483]",
                            ),
                            rx.el.div(
                                rx.el.label(
                                    rx.el.span(
                                        "Start date",
                                        class_name="mb-2 block text-sm font-semibold text-[#182333]",
                                    ),
                                    rx.el.input(
                                        type="date",
                                        default_value=CampusState.request_start,
                                        on_change=CampusState.set_request_start,
                                        class_name=FIELD,
                                    ),
                                    class_name="block",
                                ),
                                rx.el.label(
                                    rx.el.span(
                                        "Return date",
                                        class_name="mb-2 block text-sm font-semibold text-[#182333]",
                                    ),
                                    rx.el.input(
                                        type="date",
                                        default_value=CampusState.request_return,
                                        on_change=CampusState.set_request_return,
                                        class_name=FIELD,
                                    ),
                                    class_name="block",
                                ),
                                class_name="mt-6 grid gap-5 sm:grid-cols-2",
                            ),
                            rx.el.p(
                                CampusState.request_summary,
                                class_name="mt-4 rounded-xl bg-[#f4f6ff] px-4 py-3 text-sm font-semibold text-[#3159d8]",
                            ),
                            rx.cond(
                                CampusState.request_error != "",
                                rx.el.p(
                                    CampusState.request_error,
                                    class_name="mt-5 rounded-xl bg-red-50 px-4 py-3 text-sm text-red-600",
                                ),
                                rx.el.span(),
                            ),
                            rx.el.form(
                                rx.el.label(
                                    rx.el.span(
                                        "Why do you need it?",
                                        class_name="mb-2 block text-sm font-semibold text-[#182333]",
                                    ),
                                    rx.el.textarea(
                                        name="reason",
                                        rows=3,
                                        placeholder="Tell the owner what you're working on…",
                                        class_name=FIELD,
                                    ),
                                    class_name="block",
                                ),
                                rx.el.label(
                                    rx.el.span(
                                        "Message to owner (optional)",
                                        class_name="mb-2 block text-sm font-semibold text-[#182333]",
                                    ),
                                    rx.el.textarea(
                                        name="message",
                                        rows=3,
                                        placeholder="Anything else they should know?",
                                        class_name=FIELD,
                                    ),
                                    class_name="block",
                                ),
                                rx.el.button(
                                    "Send borrow request",
                                    rx.icon(
                                        "arrow-right", class_name="h-4 w-4"
                                    ),
                                    type="submit",
                                    class_name=BUTTON,
                                ),
                                on_submit=CampusState.submit_request,
                                class_name="mt-5 flex flex-col gap-5",
                            ),
                            class_name="mt-5 rounded-2xl border border-[#e6e5dd] bg-white p-6 sm:p-8",
                        ),
                    ),
                ),
                rx.el.span(),
            ),
            class_name="w-full pb-8",
        )
    )


def borrowings_page() -> rx.Component:
    return shell(
        rx.el.div(
            page_heading(
                "YOUR BORROWING JOURNEY",
                "My Borrowings.",
                "Follow requests, confirm pickup and returns, and leave a rating after each return.",
            ),
            error_note(),
            transaction_list(False),
            class_name="w-full pb-8",
        )
    )


def owner_requests_page() -> rx.Component:
    return shell(
        rx.el.div(
            page_heading(
                "YOUR REQUEST INBOX",
                "Requests.",
                "Review borrowers' plans, approve requests and keep track of items you lend.",
            ),
            error_note(),
            transaction_list(True),
            class_name="w-full pb-8",
        )
    )


def profile_page() -> rx.Component:
    return shell(
        rx.el.div(
            page_heading(
                "YOUR CAMPUS IDENTITY",
                "Your profile.",
                "Your sharing activity and reliability, based on completed transactions.",
            ),
            error_note(),
            rx.el.div(
                rx.el.div(
                    rx.icon("user-round", class_name="h-8 w-8 text-[#3159d8]"),
                    class_name="flex h-16 w-16 items-center justify-center rounded-2xl bg-[#e9edff]",
                ),
                rx.el.div(
                    rx.el.h2(
                        CampusState.student_name,
                        class_name="text-2xl font-bold text-[#182333]",
                    ),
                    rx.el.p(
                        CampusState.student_email,
                        class_name="mt-1 text-sm text-[#697483]",
                    ),
                    rx.el.p(
                        f"{CampusState.student_department} · Year {CampusState.student_year}",
                        class_name="mt-1 text-sm text-[#526071]",
                    ),
                ),
                class_name="mb-6 flex flex-wrap items-center gap-5 rounded-2xl border border-[#e6e5dd] bg-white p-6",
            ),
            rx.el.div(
                metric("Items listed", CampusState.profile_listed),
                metric("Borrowed", CampusState.profile_borrowed),
                metric("Lent", CampusState.profile_lent),
                metric("Successful returns", CampusState.profile_returns),
                metric("Late returns", CampusState.profile_late),
                rx.el.div(
                    rx.el.p(
                        "Average reliability rating",
                        class_name="text-xs font-semibold uppercase tracking-wide text-[#697483]",
                    ),
                    rx.el.p(
                        rx.cond(
                            CampusState.profile_rating_count > 0,
                            f"{CampusState.profile_rating:.1f} / 5",
                            "Not rated yet",
                        ),
                        class_name="mt-3 text-2xl font-bold text-[#182333]",
                    ),
                    rx.el.p(
                        f"Based on {CampusState.profile_rating_count} received ratings",
                        class_name="mt-2 text-xs text-[#697483]",
                    ),
                    class_name="w-full rounded-2xl border border-[#e6e5dd] bg-white p-5",
                ),
                class_name="grid grid-cols-2 gap-4 lg:grid-cols-3",
            ),
            class_name="w-full pb-8",
        )
    )


def admin_page() -> rx.Component:
    return rx.cond(
        CampusState.student_admin,
        shell(
            rx.el.div(
                page_heading(
                    "COMMUNITY OVERVIEW",
                    "Admin statistics.",
                    "Live figures from the CampusShare community.",
                ),
                error_note(),
                rx.el.div(
                    metric("Total users", CampusState.admin_users),
                    metric("Available items", CampusState.admin_available),
                    metric("Active borrowings", CampusState.admin_active),
                    metric("Pending requests", CampusState.admin_pending),
                    metric("Successfully returned", CampusState.admin_returned),
                    class_name="grid grid-cols-2 gap-4 lg:grid-cols-3",
                ),
                class_name="w-full pb-8",
            )
        ),
        rx.el.main(class_name="h-dvh bg-[#faf9f5]"),
    )


def saved_page() -> rx.Component:
    return shell(
        rx.el.div(
            page_heading(
                "YOUR SHORTLIST",
                "Saved items.",
                "Keep the good finds close until you need them.",
            ),
            error_note(),
            item_grid(
                CampusState.saved_listings,
                "Nothing saved yet. Browse items and tap the bookmark to keep them here.",
            ),
            rx.el.a(
                "Explore the catalog →",
                href="/browse",
                class_name="mt-6 inline-block text-sm font-semibold text-[#3159d8] hover:underline",
            ),
            class_name="w-full pb-8",
        )
    )
