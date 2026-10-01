import reflex as rx

from app.components.campus_ui import BUTTON, FIELD, item_art
from app.states.campus_state import CampusState, Listing


LISTING_CATEGORIES = [
    "Books",
    "Calculators",
    "Instruments",
    "Lab Equipment",
    "Electronics",
    "Stationery",
    "Sports",
    "Accessories",
    "Other",
]


def listing_field(
    label: str, name: str, value: rx.Var[str], placeholder: str
) -> rx.Component:
    return rx.el.label(
        rx.el.span(
            label, class_name="mb-2 block text-sm font-semibold text-[#182333]"
        ),
        rx.el.input(
            name=name,
            default_value=value,
            placeholder=placeholder,
            class_name=FIELD,
        ),
        class_name="block",
    )


def listing_select(
    label: str, name: str, options: list[str], value: rx.Var[str]
) -> rx.Component:
    return rx.el.label(
        rx.el.span(
            label, class_name="mb-2 block text-sm font-semibold text-[#182333]"
        ),
        rx.el.div(
            rx.el.select(
                rx.foreach(
                    options, lambda option: rx.el.option(option, value=option)
                ),
                name=name,
                default_value=value,
                class_name=f"{FIELD} appearance-none pr-10",
            ),
            rx.icon(
                "chevron-down",
                class_name="pointer-events-none absolute right-4 top-4 h-4 w-4 text-[#697483]",
            ),
            class_name="relative",
        ),
        class_name="block",
    )


def listing_form() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "SHARE SOMETHING USEFUL",
                    class_name="text-xs font-bold tracking-[0.16em] text-[#3159d8]",
                ),
                rx.el.h2(
                    rx.cond(
                        CampusState.editing_id > 0,
                        "Edit your listing",
                        "List an item",
                    ),
                    class_name="mt-2 text-2xl font-bold text-[#182333]",
                ),
                class_name="flex-1",
            ),
            rx.cond(
                CampusState.editing_id > 0,
                rx.el.button(
                    "Cancel edit",
                    on_click=CampusState.new_listing,
                    class_name="rounded-xl border border-[#dddcd5] px-4 py-2 text-sm font-semibold text-[#526071] hover:bg-[#f4f6ff]",
                ),
                rx.el.span(),
            ),
            class_name="flex items-center gap-4",
        ),
        rx.el.p(
            "Fill in the details fellow students need to borrow with confidence.",
            class_name="mt-2 text-sm text-[#697483]",
        ),
        rx.el.div(
            rx.upload.root(
                rx.icon("image-up", class_name="h-6 w-6 text-[#3159d8]"),
                rx.el.p(
                    "Choose a photo",
                    class_name="mt-2 text-sm font-semibold text-[#182333]",
                ),
                rx.el.p(
                    "JPG, PNG or WebP · up to 5 MB",
                    class_name="mt-1 text-xs text-[#697483]",
                ),
                id="listing_photo",
                max_files=1,
                multiple=False,
                accept={
                    "image/jpeg": [".jpg", ".jpeg"],
                    "image/png": [".png"],
                    "image/webp": [".webp"],
                },
                class_name="flex min-h-36 cursor-pointer flex-col items-center justify-center rounded-2xl border border-dashed border-[#bcc8fa] bg-[#f4f6ff] px-6 py-4 text-center hover:bg-[#e9edff]",
            ),
            rx.el.div(
                rx.foreach(
                    rx.selected_files("listing_photo"),
                    lambda name: rx.el.p(
                        name, class_name="truncate text-xs text-[#526071]"
                    ),
                ),
                rx.el.button(
                    "Upload selected photo",
                    type="button",
                    on_click=CampusState.upload_listing_image(
                        rx.upload_files(upload_id="listing_photo")
                    ),
                    class_name="mt-2 rounded-xl border border-[#c8d2ff] bg-white px-4 py-2 text-sm font-semibold text-[#3159d8] hover:bg-[#e9edff]",
                ),
                rx.cond(
                    CampusState.draft_image != "",
                    rx.el.img(
                        src=rx.get_upload_url(CampusState.draft_image),
                        alt="Listing photo preview",
                        class_name="mt-3 h-28 w-40 rounded-xl object-cover",
                    ),
                    rx.el.span(),
                ),
                class_name="min-w-0",
            ),
            class_name="mt-6 grid gap-4 sm:grid-cols-2",
        ),
        rx.cond(
            CampusState.listing_error != "",
            rx.el.p(
                CampusState.listing_error,
                class_name="mt-5 rounded-xl bg-red-50 px-4 py-3 text-sm font-medium text-red-600",
            ),
            rx.el.span(),
        ),
        rx.cond(
            CampusState.listing_success != "",
            rx.el.p(
                CampusState.listing_success,
                class_name="mt-5 rounded-xl bg-[#e9f7c5] px-4 py-3 text-sm font-medium text-[#344915]",
            ),
            rx.el.span(),
        ),
        rx.el.form(
            rx.el.div(
                listing_field(
                    "Item name",
                    "name",
                    CampusState.editing_item["name"],
                    "e.g. Scientific calculator",
                ),
                listing_select(
                    "Category",
                    "category",
                    LISTING_CATEGORIES,
                    CampusState.editing_item["category"],
                ),
                class_name="grid gap-5 sm:grid-cols-2",
            ),
            rx.el.label(
                rx.el.span(
                    "Description",
                    class_name="mb-2 block text-sm font-semibold text-[#182333]",
                ),
                rx.el.textarea(
                    name="description",
                    default_value=CampusState.editing_item["description"],
                    placeholder="What's included? Anything a borrower should know?",
                    rows=4,
                    class_name=FIELD,
                ),
                class_name="block",
            ),
            rx.el.div(
                listing_select(
                    "Condition",
                    "condition",
                    ["Like new", "Good", "Fair"],
                    CampusState.editing_item["condition"],
                ),
                listing_field(
                    "Pickup location",
                    "pickup_location",
                    CampusState.editing_item["pickup_location"],
                    "e.g. Library entrance",
                ),
                class_name="grid gap-5 sm:grid-cols-2",
            ),
            rx.el.div(
                rx.el.label(
                    rx.el.span(
                        "Preferred duration (days)",
                        class_name="mb-2 block text-sm font-semibold text-[#182333]",
                    ),
                    rx.el.input(
                        name="duration",
                        type="number",
                        min="1",
                        max="365",
                        default_value=CampusState.editing_item[
                            "preferred_duration_days"
                        ].to_string(),
                        class_name=FIELD,
                    ),
                    class_name="block",
                ),
                listing_select(
                    "Availability",
                    "available",
                    ["true", "false"],
                    rx.cond(
                        CampusState.editing_item["available"], "true", "false"
                    ),
                ),
                class_name="grid gap-5 sm:grid-cols-2",
            ),
            rx.el.button(
                rx.cond(
                    CampusState.editing_id > 0,
                    "Save changes",
                    "Publish listing",
                ),
                rx.icon("arrow-right", class_name="h-4 w-4"),
                type="submit",
                class_name=BUTTON,
            ),
            on_submit=CampusState.save_listing,
            key=CampusState.listing_form_revision,
            class_name="mt-6 flex flex-col gap-5",
        ),
        class_name="rounded-3xl border border-[#e6e5dd] bg-white p-6 sm:p-8",
    )


def owner_item_row(item: Listing) -> rx.Component:
    return rx.el.article(
        rx.el.a(
            item_art(item),
            href=f"/items/{item['id']}",
            class_name="h-28 w-full overflow-hidden rounded-xl sm:w-36 sm:shrink-0",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    item["name"],
                    class_name="text-base font-bold text-[#182333]",
                ),
                rx.el.span(
                    rx.cond(item["available"], "Available", "Unavailable"),
                    class_name=rx.cond(
                        item["available"],
                        "w-fit rounded-full bg-[#e9f7c5] px-3 py-1 text-xs font-bold text-[#344915]",
                        "w-fit rounded-full bg-[#efeeea] px-3 py-1 text-xs font-bold text-[#697483]",
                    ),
                ),
                class_name="flex flex-wrap items-center justify-between gap-2",
            ),
            rx.el.p(
                f"{item['category']} · {item['condition']} · {item['preferred_duration_days']} days",
                class_name="mt-2 text-sm text-[#697483]",
            ),
            rx.el.div(
                rx.el.a(
                    "Edit listing",
                    href="#listing-form",
                    on_click=lambda: CampusState.edit_listing(item["id"]),
                    class_name="rounded-xl border border-[#c8d2ff] bg-white px-4 py-2 text-xs font-semibold text-[#3159d8] hover:bg-[#e9edff]",
                ),
                rx.el.button(
                    rx.cond(
                        item["available"], "Mark unavailable", "Mark available"
                    ),
                    on_click=lambda: CampusState.toggle_item_availability(
                        item["id"]
                    ),
                    class_name="rounded-xl border border-[#dddcd5] bg-white px-4 py-2 text-xs font-semibold text-[#526071] hover:bg-[#faf9f5]",
                ),
                rx.el.a(
                    "View details →",
                    href=f"/items/{item['id']}",
                    class_name="text-xs font-semibold text-[#3159d8] hover:underline",
                ),
                class_name="mt-4 flex flex-wrap items-center gap-2",
            ),
            class_name="min-w-0 flex-1",
        ),
        class_name="flex flex-col gap-4 rounded-2xl border border-[#e6e5dd] bg-white p-4 sm:flex-row",
    )
