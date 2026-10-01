import reflex as rx

from app.components.campus_ui import BUTTON, FIELD, filter_select
from app.states.campus_state import CampusState, Transaction


def transaction_feedback() -> rx.Component:
    return rx.el.div(
        rx.cond(
            CampusState.transaction_error != "",
            rx.el.p(
                CampusState.transaction_error,
                class_name="mb-4 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-600",
            ),
            rx.el.span(),
        ),
        rx.cond(
            CampusState.transaction_success != "",
            rx.el.p(
                CampusState.transaction_success,
                class_name="mb-4 rounded-xl border border-[#cce79b] bg-[#f4fae9] p-4 text-sm text-[#344915]",
            ),
            rx.el.span(),
        ),
    )


def rating_form(transaction: Transaction) -> rx.Component:
    return rx.cond(
        transaction["my_score"] > 0,
        rx.el.p(
            f"Your rating: {transaction['my_score']} / 5 stars",
            class_name="text-sm font-semibold text-[#344915]",
        ),
        rx.el.form(
            rx.el.p(
                "Rate the other student",
                class_name="text-sm font-semibold text-[#182333]",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.select(
                        rx.el.option("Choose stars", value=""),
                        rx.el.option("★ 1", value="1"),
                        rx.el.option("★★ 2", value="2"),
                        rx.el.option("★★★ 3", value="3"),
                        rx.el.option("★★★★ 4", value="4"),
                        rx.el.option("★★★★★ 5", value="5"),
                        name="score",
                        required=True,
                        default_value="",
                        class_name=f"{FIELD} appearance-none pr-10",
                    ),
                    rx.icon(
                        "chevron-down",
                        class_name="pointer-events-none absolute right-3 top-4 h-4 w-4 text-[#697483]",
                    ),
                    class_name="relative min-w-40",
                ),
                rx.el.input(
                    name="comment",
                    placeholder="Optional comment (up to 500 characters)",
                    max_length=500,
                    class_name=FIELD,
                ),
                rx.el.button("Submit rating", type="submit", class_name=BUTTON),
                class_name="mt-3 flex flex-col gap-3 sm:flex-row",
            ),
            on_submit=lambda form_data: CampusState.rate_transaction(
                transaction["id"], form_data
            ),
            class_name="mt-3",
        ),
    )


def transaction_card(transaction: Transaction, owner: bool) -> rx.Component:
    return rx.el.article(
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    transaction["item_name"],
                    href=f"/items/{transaction['item_id']}",
                    class_name="text-lg font-bold text-[#182333] hover:text-[#3159d8]",
                ),
                rx.el.p(
                    rx.cond(owner, "Borrower: ", "Owner: "),
                    transaction["person"],
                    class_name="mt-1 text-sm text-[#526071]",
                ),
                class_name="min-w-0",
            ),
            rx.el.span(
                rx.cond(
                    transaction["overdue"],
                    "Overdue",
                    rx.cond(
                        transaction["due_soon"],
                        "Due soon",
                        transaction["status"],
                    ),
                ),
                class_name=rx.cond(
                    transaction["status"] == "returned",
                    "w-fit shrink-0 rounded-full bg-[#e9f7c5] px-3 py-1 text-xs font-bold capitalize text-[#344915]",
                    rx.cond(
                        transaction["overdue"],
                        "w-fit shrink-0 rounded-full bg-red-100 px-3 py-1 text-xs font-bold text-red-600",
                        "w-fit shrink-0 rounded-full bg-[#e9edff] px-3 py-1 text-xs font-bold capitalize text-[#3159d8]",
                    ),
                ),
            ),
            class_name="flex flex-wrap items-start justify-between gap-3",
        ),
        rx.el.div(
            rx.el.p(
                f"Pickup: {transaction['start']}",
                class_name="text-sm text-[#526071]",
            ),
            rx.el.p(
                f"Expected return: {transaction['due']}",
                class_name="text-sm text-[#526071]",
            ),
            rx.cond(
                transaction["returned"] != "",
                rx.el.p(
                    f"Returned: {transaction['returned']}",
                    class_name="text-sm font-semibold text-[#344915]",
                ),
                rx.el.span(),
            ),
            class_name="mt-4 flex flex-wrap gap-x-6 gap-y-1",
        ),
        rx.cond(
            owner,
            rx.el.div(
                rx.el.p(
                    "Reason",
                    class_name="text-xs font-bold uppercase tracking-wide text-[#697483]",
                ),
                rx.el.p(
                    transaction["reason"],
                    class_name="mt-1 whitespace-pre-wrap text-sm text-[#182333]",
                ),
                rx.cond(
                    transaction["message"] != "",
                    rx.el.p(
                        f"Message: {transaction['message']}",
                        class_name="mt-2 whitespace-pre-wrap text-sm text-[#526071]",
                    ),
                    rx.el.span(),
                ),
                class_name="mt-4 rounded-xl bg-[#faf9f5] p-4",
            ),
            rx.el.span(),
        ),
        rx.el.div(
            rx.cond(
                rx.cond(owner, transaction["status"] == "pending", False),
                rx.el.div(
                    rx.el.button(
                        "Accept request",
                        on_click=lambda: CampusState.decide_request(
                            transaction["id"], True
                        ),
                        class_name=BUTTON,
                    ),
                    rx.el.button(
                        "Reject",
                        on_click=lambda: CampusState.decide_request(
                            transaction["id"], False
                        ),
                        class_name="rounded-xl border border-[#dddcd5] bg-white px-5 py-3 text-sm font-semibold text-[#526071] hover:bg-red-50",
                    ),
                    class_name="flex flex-wrap gap-3",
                ),
                rx.el.span(),
            ),
            rx.cond(
                transaction["status"] == "approved",
                rx.el.button(
                    "Confirm pickup",
                    on_click=lambda: CampusState.advance_borrowing(
                        transaction["id"], False
                    ),
                    class_name=BUTTON,
                ),
                rx.el.span(),
            ),
            rx.cond(
                transaction["status"] == "active",
                rx.el.button(
                    "Confirm return",
                    on_click=lambda: CampusState.advance_borrowing(
                        transaction["id"], True
                    ),
                    class_name=BUTTON,
                ),
                rx.el.span(),
            ),
            rx.cond(
                transaction["status"] == "returned",
                rx.el.div(
                    rx.el.p(
                        rx.cond(
                            transaction["other_score"] > 0,
                            f"Other student rated you {transaction['other_score']} / 5 stars",
                            "Other student's rating is pending",
                        ),
                        class_name="text-xs text-[#697483]",
                    ),
                    rating_form(transaction),
                    class_name="w-full",
                ),
                rx.el.span(),
            ),
            class_name="mt-5 border-t border-[#ecebe4] pt-4",
        ),
        class_name="rounded-2xl border border-[#e6e5dd] bg-white p-5 sm:p-6",
    )


def transaction_list(owner: bool) -> rx.Component:
    return rx.el.div(
        transaction_feedback(),
        rx.el.div(
            filter_select(
                "Show",
                rx.cond(
                    owner,
                    [
                        "All",
                        "Pending",
                        "Approved",
                        "Active",
                        "Returned",
                        "Rejected",
                    ],
                    [
                        "All",
                        "Pending",
                        "Approved",
                        "Active",
                        "Due soon",
                        "Returned",
                        "Rejected",
                    ],
                ),
                rx.cond(
                    owner, CampusState.request_filter, CampusState.borrow_filter
                ),
                CampusState.set_transaction_filter,
            ),
            class_name="mb-5 max-w-xs",
        ),
        rx.cond(
            rx.cond(
                owner,
                CampusState.visible_owner_requests,
                CampusState.visible_borrowings,
            ).length()
            > 0,
            rx.el.div(
                rx.foreach(
                    rx.cond(
                        owner,
                        CampusState.visible_owner_requests,
                        CampusState.visible_borrowings,
                    ),
                    lambda transaction: transaction_card(transaction, owner),
                ),
                class_name="flex flex-col gap-4",
            ),
            rx.el.div(
                rx.icon("inbox", class_name="mx-auto h-9 w-9 text-[#3159d8]"),
                rx.el.p(
                    rx.cond(
                        owner,
                        "No requests in this view yet. New requests will appear here.",
                        "Nothing in this view yet. Browse items to find something useful to borrow.",
                    ),
                    class_name="mt-3 text-sm text-[#697483]",
                ),
                rx.el.a(
                    "Browse items →",
                    href="/browse",
                    class_name="mt-3 inline-block text-sm font-semibold text-[#3159d8] hover:underline",
                ),
                class_name="rounded-2xl border border-dashed border-[#d8d9d5] bg-white px-6 py-12 text-center",
            ),
        ),
    )


def metric(
    label: str, value: rx.Var[int] | rx.Var[float], suffix: str = ""
) -> rx.Component:
    return rx.el.div(
        rx.el.p(
            label,
            class_name="text-xs font-semibold uppercase tracking-wide text-[#697483]",
        ),
        rx.el.p(
            f"{value}{suffix}",
            class_name="mt-3 text-3xl font-bold text-[#182333]",
        ),
        class_name="w-full rounded-2xl border border-[#e6e5dd] bg-white p-5",
    )
