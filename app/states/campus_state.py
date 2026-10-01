import reflex as rx
import hashlib
import hmac
import logging
import re
import secrets
from datetime import date, timedelta
from uuid import uuid4
from typing import Any, TypedDict

from faker import Faker
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError


DEMO_PASSWORD = "CampusDemo2026!"
CATEGORIES = [
    "All",
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


class Listing(TypedDict):
    id: int
    name: str
    category: str
    description: str
    condition: str
    available: bool
    image_path: str
    pickup_location: str
    preferred_duration_days: int
    owner: str
    department: str
    year: int
    saved: bool
    own: bool


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(32)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 350000)
    return f"pbkdf2_sha256$350000${salt.hex()}${digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    try:
        algorithm, iterations, salt, digest = stored.split("$")
        if (
            algorithm != "pbkdf2_sha256"
            or not 100000 <= int(iterations) <= 1000000
        ):
            return False
        candidate = hashlib.pbkdf2_hmac(
            "sha256", password.encode(), bytes.fromhex(salt), int(iterations)
        )
        return hmac.compare_digest(candidate, bytes.fromhex(digest))
    except (ValueError, TypeError):
        return False


SEED_ITEMS = [
    (
        "Canon EOS Rebel T7 camera",
        "Electronics",
        "DSLR camera with 18–55mm lens, battery and carrying bag. Great for photo assignments.",
        "Good",
        "Library entrance",
        5,
    ),
    (
        "TI-84 Plus graphing calculator",
        "Calculators",
        "Fresh batteries included. Perfect for calculus and statistics exams.",
        "Like new",
        "Engineering atrium",
        3,
    ),
    (
        "The Design of Everyday Things",
        "Books",
        "Don Norman paperback with a few penciled notes in the margins.",
        "Good",
        "Design building",
        14,
    ),
    (
        "Bosch cordless drill kit",
        "Other",
        "Drill, charger, bits and carrying case for dorm or project work.",
        "Good",
        "North residence hall",
        2,
    ),
    (
        "Two-person camping tent",
        "Other",
        "Lightweight tent with stakes and rain fly. Clean and ready for a weekend away.",
        "Like new",
        "Student union",
        4,
    ),
    (
        "Instant Pot 6-quart cooker",
        "Other",
        "Pressure cooker with inner pot and lid; ideal for a shared kitchen.",
        "Good",
        "West residence hall",
        7,
    ),
    (
        "Yonex badminton set",
        "Sports",
        "Two rackets and shuttlecocks for an afternoon on the courts.",
        "Good",
        "Recreation center",
        3,
    ),
    (
        "Wacom drawing tablet",
        "Electronics",
        "Compact pen tablet with USB cable and stylus for digital illustration.",
        "Like new",
        "Arts studio",
        5,
    ),
    (
        "Portable projector",
        "Electronics",
        "Mini projector with HDMI cable for presentations and movie nights.",
        "Good",
        "Science hall",
        2,
    ),
    (
        "Organic chemistry study guide",
        "Books",
        "Annotated revision guide with reaction summaries and practice questions.",
        "Fair",
        "Science library",
        14,
    ),
    (
        "Bike repair tool roll",
        "Accessories",
        "Hex keys, tire levers, pump and patch kit for quick fixes.",
        "Good",
        "Bike hub",
        3,
    ),
    (
        "Yoga mat and blocks",
        "Sports",
        "Clean mat and two foam blocks, easy to carry across campus.",
        "Like new",
        "Recreation center",
        5,
    ),
    (
        "Casio fx-991EX scientific calculator",
        "Calculators",
        "Casio scientific calculator with fresh batteries and a protective cover. Handy for tomorrow's chemistry or engineering exam.",
        "Like new",
        "Engineering atrium",
        3,
    ),
    (
        "Acoustic guitar with soft case",
        "Instruments",
        "Full-size acoustic guitar, tuned and ready for music practice. Includes a soft carrying case.",
        "Good",
        "Music building lobby",
        7,
    ),
    (
        "Introduction to Algorithms textbook",
        "Books",
        "Third-edition course textbook with clean pages and a few removable page markers.",
        "Good",
        "Main library entrance",
        14,
    ),
    (
        "Student microscope kit",
        "Lab Equipment",
        "Portable microscope with slides and lens cloth for supervised biology coursework.",
        "Good",
        "Biology building front desk",
        3,
    ),
    (
        "Safety goggles and lab coat",
        "Lab Equipment",
        "Clean medium lab coat and splash-resistant goggles for practical sessions.",
        "Like new",
        "Science hall entrance",
        5,
    ),
    (
        "Drafting pencil and ruler set",
        "Stationery",
        "Mechanical pencils, spare leads, scale ruler and eraser for drawing and design classes.",
        "Good",
        "Design building lobby",
        7,
    ),
    (
        "USB-C adapter and HDMI cable",
        "Accessories",
        "Compact USB-C to HDMI adapter and cable for classroom presentations; tested with a laptop.",
        "Like new",
        "Student union help desk",
        4,
    ),
    (
        "Portable whiteboard and markers",
        "Other",
        "Small dry-erase board with markers and eraser for group study sessions.",
        "Good",
        "Main library entrance",
        2,
    ),
]

LEGACY_SEED_CATEGORIES = {
    "Canon EOS Rebel T7 camera": "Creative",
    "TI-84 Plus graphing calculator": "Electronics",
    "Bosch cordless drill kit": "Tools",
    "Two-person camping tent": "Outdoor",
    "Instant Pot 6-quart cooker": "Kitchen",
    "Wacom drawing tablet": "Creative",
    "Bike repair tool roll": "Tools",
}


async def seed_demo() -> None:
    """Seed a small repeatable showcase catalog, serialized across concurrent first visits."""
    fake = Faker()
    fake.seed_instance(412)
    emails = [
        "alex@campusshare.demo",
        "maya@campusshare.demo",
        "jordan@campusshare.demo",
        "sam@campusshare.demo",
    ]
    departments = [
        "Computer Science",
        "Visual Arts",
        "Mechanical Engineering",
        "Biology",
    ]
    try:
        async with rx.asession() as session:
            await session.execute(text("SELECT pg_advisory_xact_lock(2471186)"))
            for index, email in enumerate(emails):
                existing = (
                    await session.execute(
                        text("SELECT id FROM student WHERE email = :email"),
                        {"email": email},
                    )
                ).scalar_one_or_none()
                if existing is None:
                    await session.execute(
                        text(
                            "INSERT INTO student (email, password_hash, name, department, year, is_admin) VALUES (:email, :password_hash, :name, :department, :year, :is_admin)"
                        ),
                        {
                            "email": email,
                            "password_hash": hash_password(DEMO_PASSWORD),
                            "name": fake.name(),
                            "department": departments[index],
                            "year": index + 1,
                            "is_admin": index == 0,
                        },
                    )
            owners = (
                await session.execute(
                    text(
                        "SELECT id, email FROM student WHERE email IN (:email_0, :email_1, :email_2, :email_3)"
                    ),
                    {f"email_{i}": email for i, email in enumerate(emails)},
                )
            ).all()
            owner_ids = {row.email: row.id for row in owners}
            for index, (
                name,
                category,
                description,
                condition,
                location,
                duration,
            ) in enumerate(SEED_ITEMS):
                owner_id = owner_ids[emails[index % len(emails)]]
                present = (
                    await session.execute(
                        text(
                            "SELECT id FROM item WHERE owner_student_id = :owner AND name = :name LIMIT 1"
                        ),
                        {"owner": owner_id, "name": name},
                    )
                ).scalar_one_or_none()
                if present is None:
                    await session.execute(
                        text(
                            "INSERT INTO item (owner_student_id, name, category, description, condition, available, image_path, preferred_duration_days, pickup_location) VALUES (:owner, :name, :category, :description, :condition, true, '', :duration, :location)"
                        ),
                        {
                            "owner": owner_id,
                            "name": name,
                            "category": category,
                            "description": description,
                            "condition": condition,
                            "duration": duration,
                            "location": location,
                        },
                    )
                elif name in LEGACY_SEED_CATEGORIES:
                    await session.execute(
                        text(
                            "UPDATE item SET category = :category WHERE id = :id AND category = :legacy_category"
                        ),
                        {
                            "id": present,
                            "category": category,
                            "legacy_category": LEGACY_SEED_CATEGORIES[name],
                        },
                    )
            demo_item = (
                await session.execute(
                    text(
                        "SELECT id, available FROM item WHERE owner_student_id = :owner AND name = :name LIMIT 1"
                    ),
                    {
                        "owner": owner_ids[emails[0]],
                        "name": "Casio fx-991EX scientific calculator",
                    },
                )
            ).first()
            if demo_item and demo_item.available:
                past_request = (
                    await session.execute(
                        text(
                            "SELECT id FROM borrow_request WHERE item_id = :item AND borrower_student_id = :borrower LIMIT 1"
                        ),
                        {
                            "item": demo_item.id,
                            "borrower": owner_ids[emails[1]],
                        },
                    )
                ).first()
                if past_request is None:
                    await session.execute(
                        text(
                            "INSERT INTO borrow_request (item_id, borrower_student_id, lender_student_id, start_date, expected_return_date, reason, message, status) VALUES (:item, :borrower, :lender, CURRENT_DATE, CURRENT_DATE + 1, :reason, :message, 'pending')"
                        ),
                        {
                            "item": demo_item.id,
                            "borrower": owner_ids[emails[1]],
                            "lender": owner_ids[emails[0]],
                            "reason": "I need a scientific calculator for tomorrow's chemistry exam.",
                            "message": "I can collect it at the engineering atrium.",
                        },
                    )
            await session.commit()
    except Exception as e:
        logging.exception(f"Error: {e}")
        raise


LISTING_COLUMNS = """i.id, i.name, i.category, i.description, i.condition, i.available,
i.image_path, i.pickup_location, i.preferred_duration_days, s.name AS owner,
s.department, s.year, CASE WHEN si.id IS NULL THEN false ELSE true END AS saved,
CASE WHEN i.owner_student_id = :viewer THEN true ELSE false END AS own"""
LISTING_JOINS = """FROM item i JOIN student s ON s.id = i.owner_student_id
LEFT JOIN saved_item si ON si.item_id = i.id AND si.student_id = :viewer"""


def listing_from_row(row: Any) -> Listing:
    return {
        "id": row.id,
        "name": row.name,
        "category": row.category,
        "description": row.description or "",
        "condition": row.condition,
        "available": row.available,
        "image_path": row.image_path or "",
        "pickup_location": row.pickup_location or "",
        "preferred_duration_days": row.preferred_duration_days,
        "owner": row.owner,
        "department": row.department or "",
        "year": row.year,
        "saved": row.saved,
        "own": row.own,
    }


class Transaction(TypedDict):
    id: int
    item_id: int
    item_name: str
    person: str
    start: str
    due: str
    returned: str
    reason: str
    message: str
    status: str
    due_soon: bool
    overdue: bool
    my_score: int
    other_score: int


def transaction_from_row(row: Any) -> Transaction:
    today = date.today()
    return {
        "id": row.id,
        "item_id": row.item_id,
        "item_name": row.item_name,
        "person": row.person,
        "start": row.start_date.isoformat(),
        "due": row.expected_return_date.isoformat(),
        "returned": row.actual_return_date.isoformat()
        if row.actual_return_date
        else "",
        "reason": row.reason,
        "message": row.message or "",
        "status": row.status,
        "due_soon": row.status == "active"
        and today <= row.expected_return_date <= today + timedelta(days=2),
        "overdue": row.status == "active" and row.expected_return_date < today,
        "my_score": row.my_score or 0,
        "other_score": row.other_score or 0,
    }


class CampusState(rx.State):
    _student_id: int = 0
    student_name: str = ""
    student_email: str = ""
    student_department: str = ""
    student_year: int = 1
    student_admin: bool = False
    auth_error: str = ""
    page_error: str = ""
    search: str = ""
    need_query: str = ""
    need_searched: bool = False
    category: str = "All"
    availability: str = "All"
    condition_filter: str = "All"
    department_filter: str = "All"
    year_filter: str = "All"
    location_filter: str = "All"
    department_options: list[str] = ["All"]
    location_options: list[str] = ["All"]
    home_recent: list[Listing] = []
    home_popular: list[Listing] = []
    home_nearby: list[Listing] = []
    need_results: list[Listing] = []
    listings: list[Listing] = []
    saved_listings: list[Listing] = []
    selected_item: Listing = {
        "id": 0,
        "name": "",
        "category": "",
        "description": "",
        "condition": "",
        "available": False,
        "image_path": "",
        "pickup_location": "",
        "preferred_duration_days": 0,
        "owner": "",
        "department": "",
        "year": 1,
        "saved": False,
        "own": False,
    }
    detail_found: bool = False
    categories: list[str] = CATEGORIES
    my_items: list[Listing] = []
    editing_id: int = 0
    listing_form_revision: int = 0
    editing_item: Listing = dict(
        id=0,
        name="",
        category="Books",
        description="",
        condition="Good",
        available=True,
        image_path="",
        pickup_location="",
        preferred_duration_days=7,
        owner="",
        department="",
        year=1,
        saved=False,
        own=True,
    )
    draft_image: str = ""
    listing_error: str = ""
    listing_success: str = ""
    request_error: str = ""
    request_sent: bool = False
    request_start: str = ""
    request_return: str = ""
    borrowings: list[Transaction] = []
    owner_requests: list[Transaction] = []
    transaction_error: str = ""
    transaction_success: str = ""
    borrow_filter: str = "All"
    request_filter: str = "Pending"
    profile_listed: int = 0
    profile_borrowed: int = 0
    profile_lent: int = 0
    profile_returns: int = 0
    profile_late: int = 0
    profile_rating: float = 0.0
    profile_rating_count: int = 0
    admin_users: int = 0
    admin_available: int = 0
    admin_active: int = 0
    admin_pending: int = 0
    admin_returned: int = 0

    @rx.var
    def visible_borrowings(self) -> list[Transaction]:
        if self.borrow_filter == "All":
            return self.borrowings
        if self.borrow_filter == "Due soon":
            return [r for r in self.borrowings if r["due_soon"] or r["overdue"]]
        return [
            r
            for r in self.borrowings
            if r["status"] == self.borrow_filter.lower()
        ]

    @rx.var
    def visible_owner_requests(self) -> list[Transaction]:
        if self.request_filter == "All":
            return self.owner_requests
        return [
            r
            for r in self.owner_requests
            if r["status"] == self.request_filter.lower()
        ]

    @rx.event
    def set_borrow_filter(self, value: str):
        self.borrow_filter = (
            value
            if value
            in (
                "All",
                "Pending",
                "Approved",
                "Active",
                "Due soon",
                "Returned",
                "Rejected",
            )
            else "All"
        )

    @rx.event
    def set_request_filter(self, value: str):
        self.request_filter = (
            value
            if value
            in ("All", "Pending", "Approved", "Active", "Returned", "Rejected")
            else "Pending"
        )

    @rx.event
    def set_transaction_filter(self, value: str):
        if self.router.url.path.startswith("/requests"):
            self.set_request_filter(value)
        else:
            self.set_borrow_filter(value)

    async def _load_transactions(self, owner: bool):
        role = "lender" if owner else "borrower"
        other = "borrower" if owner else "lender"
        try:
            async with rx.asession() as session:
                rows = (
                    await session.execute(
                        text(f"""
                    SELECT b.id, b.item_id, i.name AS item_name, s.name AS person,
                    b.start_date, b.expected_return_date, b.actual_return_date,
                    b.reason, b.message, b.status,
                    (SELECT score FROM rating WHERE request_id = b.id AND rater_student_id = :viewer) AS my_score,
                    (SELECT score FROM rating WHERE request_id = b.id AND rated_student_id = :viewer) AS other_score
                    FROM borrow_request b JOIN item i ON i.id = b.item_id
                    JOIN student s ON s.id = b.{other}_student_id
                    WHERE b.{role}_student_id = :viewer
                    ORDER BY b.created_at DESC, b.id DESC LIMIT 100
                """),
                        {"viewer": self._student_id},
                    )
                ).all()
            if owner:
                self.owner_requests = [
                    transaction_from_row(row) for row in rows
                ]
            else:
                self.borrowings = [transaction_from_row(row) for row in rows]
            self.page_error = ""
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.page_error = (
                "Transactions couldn't be loaded. Please refresh and try again."
            )

    @rx.event
    async def load_borrowings(self):
        if not await self._guard():
            return rx.redirect("/login")
        self.transaction_error = ""
        self.transaction_success = ""
        await self._load_transactions(False)

    @rx.event
    async def load_owner_requests(self):
        if not await self._guard():
            return rx.redirect("/login")
        self.transaction_error = ""
        self.transaction_success = ""
        await self._load_transactions(True)

    @rx.event
    async def decide_request(self, request_id: int, accept: bool):
        if not await self._guard():
            return rx.redirect("/login")
        self.transaction_error = ""
        self.transaction_success = ""
        try:
            async with rx.asession() as session:
                candidate = (
                    await session.execute(
                        text(
                            "SELECT item_id FROM borrow_request WHERE id = :id"
                        ),
                        {"id": request_id},
                    )
                ).first()
                if candidate is None:
                    self.transaction_error = (
                        "Request not found. Refresh this page."
                    )
                    return
                item = (
                    await session.execute(
                        text(
                            "SELECT id, owner_student_id, available FROM item WHERE id = :id FOR UPDATE"
                        ),
                        {"id": candidate.item_id},
                    )
                ).first()
                request = (
                    await session.execute(
                        text(
                            "SELECT lender_student_id, status, start_date, expected_return_date FROM borrow_request WHERE id = :id AND item_id = :item FOR UPDATE"
                        ),
                        {"id": request_id, "item": candidate.item_id},
                    )
                ).first()
                if (
                    item is None
                    or request is None
                    or item.owner_student_id != self._student_id
                    or request.lender_student_id != self._student_id
                ):
                    self.transaction_error = "You cannot manage this request."
                    return
                if request.status != "pending":
                    self.transaction_error = "This request has already been decided. Refresh to see its status."
                    return
                if accept:
                    if (
                        not item.available
                        or request.expected_return_date < date.today()
                    ):
                        self.transaction_error = "This item is unavailable or the requested dates have passed. Reject this request instead."
                        return
                    busy = (
                        await session.execute(
                            text(
                                "SELECT id FROM borrow_request WHERE item_id = :item AND status IN ('approved', 'active') LIMIT 1"
                            ),
                            {"item": item.id},
                        )
                    ).first()
                    if busy:
                        self.transaction_error = (
                            "This item already has an approved borrowing."
                        )
                        return
                    await session.execute(
                        text(
                            "UPDATE borrow_request SET status = 'approved', updated_at = CURRENT_TIMESTAMP WHERE id = :id"
                        ),
                        {"id": request_id},
                    )
                    await session.execute(
                        text(
                            "UPDATE borrow_request SET status = 'rejected', updated_at = CURRENT_TIMESTAMP WHERE item_id = :item AND id <> :id AND status = 'pending'"
                        ),
                        {"item": item.id, "id": request_id},
                    )
                    await session.execute(
                        text(
                            "UPDATE item SET available = false, updated_at = CURRENT_TIMESTAMP WHERE id = :item"
                        ),
                        {"item": item.id},
                    )
                else:
                    await session.execute(
                        text(
                            "UPDATE borrow_request SET status = 'rejected', updated_at = CURRENT_TIMESTAMP WHERE id = :id"
                        ),
                        {"id": request_id},
                    )
                await session.commit()
            self.transaction_success = (
                "Request approved. Competing requests were declined."
                if accept
                else "Request declined."
            )
            await self._load_transactions(True)
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.transaction_error = (
                "Couldn't update this request. Please try again."
            )

    @rx.event
    async def advance_borrowing(self, request_id: int, return_item: bool):
        if not await self._guard():
            return rx.redirect("/login")
        self.transaction_error = ""
        self.transaction_success = ""
        try:
            async with rx.asession() as session:
                candidate = (
                    await session.execute(
                        text(
                            "SELECT item_id FROM borrow_request WHERE id = :id"
                        ),
                        {"id": request_id},
                    )
                ).first()
                if candidate is None:
                    self.transaction_error = (
                        "Borrowing not found. Refresh the page."
                    )
                    return
                item = (
                    await session.execute(
                        text(
                            "SELECT id, owner_student_id FROM item WHERE id = :id FOR UPDATE"
                        ),
                        {"id": candidate.item_id},
                    )
                ).first()
                request = (
                    await session.execute(
                        text(
                            "SELECT borrower_student_id, lender_student_id, status, start_date FROM borrow_request WHERE id = :id AND item_id = :item FOR UPDATE"
                        ),
                        {"id": request_id, "item": candidate.item_id},
                    )
                ).first()
                if (
                    item is None
                    or request is None
                    or item.owner_student_id != request.lender_student_id
                    or self._student_id
                    not in (
                        request.borrower_student_id,
                        request.lender_student_id,
                    )
                ):
                    self.transaction_error = "You cannot update this borrowing."
                    return
                if return_item:
                    if (
                        request.status != "active"
                        or date.today() < request.start_date
                    ):
                        self.transaction_error = "Only a checked-out item can be returned on or after its start date."
                        return
                    await session.execute(
                        text(
                            "UPDATE borrow_request SET status = 'returned', actual_return_date = :today, updated_at = CURRENT_TIMESTAMP WHERE id = :id"
                        ),
                        {"today": date.today(), "id": request_id},
                    )
                    await session.execute(
                        text(
                            "UPDATE item SET available = true, updated_at = CURRENT_TIMESTAMP WHERE id = :id"
                        ),
                        {"id": item.id},
                    )
                else:
                    if (
                        request.status != "approved"
                        or date.today() < request.start_date
                    ):
                        self.transaction_error = "Pickup can be confirmed only after approval and on or after the start date."
                        return
                    await session.execute(
                        text(
                            "UPDATE borrow_request SET status = 'active', updated_at = CURRENT_TIMESTAMP WHERE id = :id"
                        ),
                        {"id": request_id},
                    )
                await session.commit()
            self.transaction_success = (
                "Return confirmed. The item is available again."
                if return_item
                else "Pickup confirmed. This borrowing is now active."
            )
            await self._load_transactions(
                self.router.url.path.startswith("/requests")
            )
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.transaction_error = (
                "Couldn't update this borrowing. Please try again."
            )

    @rx.event
    async def rate_transaction(
        self, request_id: int, form_data: dict[str, Any]
    ):
        if not await self._guard():
            return rx.redirect("/login")
        self.transaction_error = ""
        self.transaction_success = ""
        raw_score = str(form_data.get("score", ""))
        comment = str(form_data.get("comment", "")).strip()
        if raw_score not in ("1", "2", "3", "4", "5") or len(comment) > 500:
            self.transaction_error = (
                "Choose 1–5 stars and keep your comment under 500 characters."
            )
            return
        try:
            async with rx.asession() as session:
                request = (
                    await session.execute(
                        text(
                            "SELECT borrower_student_id, lender_student_id, status FROM borrow_request WHERE id = :id FOR UPDATE"
                        ),
                        {"id": request_id},
                    )
                ).first()
                if (
                    request is None
                    or request.status != "returned"
                    or self._student_id
                    not in (
                        request.borrower_student_id,
                        request.lender_student_id,
                    )
                ):
                    self.transaction_error = (
                        "Only participants can rate a returned borrowing."
                    )
                    return
                rated = (
                    request.lender_student_id
                    if self._student_id == request.borrower_student_id
                    else request.borrower_student_id
                )
                existing = (
                    await session.execute(
                        text(
                            "SELECT id FROM rating WHERE request_id = :id AND rater_student_id = :viewer"
                        ),
                        {"id": request_id, "viewer": self._student_id},
                    )
                ).first()
                if existing:
                    self.transaction_error = (
                        "You already rated this transaction."
                    )
                    return
                await session.execute(
                    text(
                        "INSERT INTO rating (request_id, rater_student_id, rated_student_id, score, comment) VALUES (:id, :rater, :rated, :score, :comment)"
                    ),
                    {
                        "id": request_id,
                        "rater": self._student_id,
                        "rated": rated,
                        "score": int(raw_score),
                        "comment": comment or None,
                    },
                )
                await session.commit()
            self.transaction_success = (
                "Thanks for rating your campus sharing experience."
            )
            await self._load_transactions(
                self.router.url.path.startswith("/requests")
            )
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.transaction_error = (
                "Couldn't save your rating. Please try again."
            )

    @rx.event
    async def load_profile(self):
        if not await self._guard():
            return rx.redirect("/login")
        self.page_error = ""
        try:
            async with rx.asession() as session:
                row = (
                    await session.execute(
                        text("""
                    SELECT (SELECT COUNT(*) FROM item WHERE owner_student_id = :id) AS listed,
                    (SELECT COUNT(*) FROM borrow_request WHERE borrower_student_id = :id AND status IN ('approved','active','returned')) AS borrowed,
                    (SELECT COUNT(*) FROM borrow_request WHERE lender_student_id = :id AND status IN ('approved','active','returned')) AS lent,
                    (SELECT COUNT(*) FROM borrow_request WHERE borrower_student_id = :id AND status = 'returned') AS returns,
                    (SELECT COUNT(*) FROM borrow_request WHERE borrower_student_id = :id AND status = 'returned' AND actual_return_date > expected_return_date) AS late,
                    (SELECT COALESCE(AVG(score),0) FROM rating WHERE rated_student_id = :id) AS rating,
                    (SELECT COUNT(*) FROM rating WHERE rated_student_id = :id) AS rating_count
                """),
                        {"id": self._student_id},
                    )
                ).one()
            self.profile_listed = row.listed
            self.profile_borrowed = row.borrowed
            self.profile_lent = row.lent
            self.profile_returns = row.returns
            self.profile_late = row.late
            self.profile_rating = float(row.rating)
            self.profile_rating_count = row.rating_count
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.page_error = (
                "Profile statistics couldn't be loaded. Please refresh."
            )

    @rx.event
    async def load_admin(self):
        if not await self._guard():
            return rx.redirect("/login")
        if not self.student_admin:
            return rx.redirect("/")
        self.page_error = ""
        try:
            async with rx.asession() as session:
                row = (
                    await session.execute(
                        text("""
                    SELECT (SELECT COUNT(*) FROM student) AS users,
                    (SELECT COUNT(*) FROM item WHERE available = true) AS available,
                    (SELECT COUNT(*) FROM borrow_request WHERE status = 'active') AS active,
                    (SELECT COUNT(*) FROM borrow_request WHERE status = 'pending') AS pending,
                    (SELECT COUNT(*) FROM borrow_request WHERE status = 'returned') AS returned
                """)
                    )
                ).one()
            self.admin_users = row.users
            self.admin_available = row.available
            self.admin_active = row.active
            self.admin_pending = row.pending
            self.admin_returned = row.returned
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.page_error = "Statistics couldn't be loaded. Please refresh."

    @rx.var
    def request_summary(self) -> str:
        try:
            start = date.fromisoformat(self.request_start)
            end = date.fromisoformat(self.request_return)
            days = (end - start).days + 1
            if days < 1:
                return "Return date must be on or after the start date."
            return f"{days} calendar day{'s' if days != 1 else ''} · Return by {end.strftime('%b %d, %Y')}"
        except ValueError:
            return "Choose both dates to see your borrowing window."

    @rx.var
    def logged_in(self) -> bool:
        return self._student_id > 0

    async def _guard(self) -> bool:
        if not self._student_id:
            return False
        async with rx.asession() as session:
            row = (
                await session.execute(
                    text(
                        "SELECT name, email, department, year, is_admin FROM student WHERE id = :id"
                    ),
                    {"id": self._student_id},
                )
            ).first()
        if row is None:
            self._student_id = 0
            return False
        self.student_name = row.name
        self.student_email = row.email
        self.student_department = row.department
        self.student_year = row.year
        self.student_admin = row.is_admin
        return True

    @rx.event
    async def load_auth(self):
        await seed_demo()
        if self._student_id:
            return rx.redirect("/")
        self.auth_error = ""

    @rx.event
    async def login(self, form_data: dict[str, Any]):
        email = str(form_data.get("email", "")).strip().lower()
        password = str(form_data.get("password", ""))
        self.auth_error = ""
        try:
            async with rx.asession() as session:
                row = (
                    await session.execute(
                        text(
                            "SELECT id, password_hash FROM student WHERE email = :email"
                        ),
                        {"email": email},
                    )
                ).first()
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.auth_error = (
                "Sign in is unavailable right now. Please try again."
            )
            return
        if row is None or not verify_password(password, row.password_hash):
            self.auth_error = "Incorrect email or password. Please try again."
            return
        self._student_id = row.id
        await self._guard()
        return rx.redirect("/")

    @rx.event
    async def signup(self, form_data: dict[str, Any]):
        name = str(form_data.get("name", "")).strip()
        email = str(form_data.get("email", "")).strip().lower()
        password = str(form_data.get("password", ""))
        department = str(form_data.get("department", "")).strip()
        raw_year = str(form_data.get("year", ""))
        self.auth_error = ""
        if not 2 <= len(name) <= 80 or not re.fullmatch(
            r"[\w .,'-]+", name, flags=re.UNICODE
        ):
            self.auth_error = "Enter a valid name (2–80 characters)."
        elif (
            not re.fullmatch(
                r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}", email
            )
            or len(email) > 254
        ):
            self.auth_error = "Enter a valid email address."
        elif (
            len(password) < 10
            or len(password) > 128
            or not re.search(r"[A-Za-z]", password)
            or not re.search(r"\d", password)
        ):
            self.auth_error = (
                "Use 10–128 characters with at least one letter and one number."
            )
        elif not 2 <= len(department) <= 80:
            self.auth_error = "Enter your department (2–80 characters)."
        elif raw_year not in ("1", "2", "3", "4", "5", "6"):
            self.auth_error = "Select a valid year of study."
        if self.auth_error:
            return
        try:
            async with rx.asession() as session:
                result = await session.execute(
                    text(
                        "INSERT INTO student (name, email, password_hash, department, year, is_admin) VALUES (:name, :email, :password_hash, :department, :year, false) RETURNING id"
                    ),
                    {
                        "name": name,
                        "email": email,
                        "password_hash": hash_password(password),
                        "department": department,
                        "year": int(raw_year),
                    },
                )
                student_id = result.scalar_one()
                await session.commit()
        except IntegrityError:
            logging.exception("Unexpected error")
            self.auth_error = (
                "This email is already registered. Sign in instead."
            )
            return
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.auth_error = (
                "Registration is unavailable right now. Please try again."
            )
            return
        self._student_id = student_id
        await self._guard()
        return rx.redirect("/")

    @rx.event
    def logout(self):
        self._student_id = 0
        self.student_name = ""
        self.student_email = ""
        self.student_admin = False
        self.listings = []
        self.saved_listings = []
        return rx.redirect("/login")

    @rx.event
    async def load_home(self):
        if not await self._guard():
            return rx.redirect("/login")
        self.page_error = ""
        try:
            async with rx.asession() as session:
                recent = (
                    await session.execute(
                        text(
                            f"SELECT {LISTING_COLUMNS} {LISTING_JOINS} WHERE i.available = true AND i.owner_student_id <> :viewer ORDER BY i.created_at DESC, i.id DESC LIMIT 4"
                        ),
                        {"viewer": self._student_id},
                    )
                ).all()
                popular = (
                    await session.execute(
                        text(
                            f"SELECT {LISTING_COLUMNS} {LISTING_JOINS} WHERE i.available = true AND i.owner_student_id <> :viewer ORDER BY (SELECT COUNT(*) FROM saved_item x WHERE x.item_id = i.id) DESC, i.id ASC LIMIT 4"
                        ),
                        {"viewer": self._student_id},
                    )
                ).all()
                nearby = (
                    await session.execute(
                        text(
                            f"SELECT {LISTING_COLUMNS} {LISTING_JOINS} WHERE i.available = true AND i.owner_student_id <> :viewer ORDER BY CASE WHEN s.department = :department THEN 0 ELSE 1 END, i.id DESC LIMIT 4"
                        ),
                        {
                            "viewer": self._student_id,
                            "department": self.student_department,
                        },
                    )
                ).all()
            self.home_recent = [listing_from_row(r) for r in recent]
            self.home_popular = [listing_from_row(r) for r in popular]
            self.home_nearby = [listing_from_row(r) for r in nearby]
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.page_error = (
                "We couldn't load items. Please refresh to try again."
            )

    @rx.event
    async def search_home(self, form_data: dict[str, Any]):
        self.search = str(form_data.get("search", "")).strip()[:120]
        self.category = "All"
        return rx.redirect("/browse")

    @rx.event
    async def need_it(self, form_data: dict[str, Any]):
        if not await self._guard():
            return rx.redirect("/login")
        self.need_query = str(form_data.get("need", "")).strip()[:200]
        self.need_searched = True
        self.need_results = []
        if not self.need_query:
            return
        words = [
            word
            for word in re.findall(r"[a-z0-9]+", self.need_query.lower())
            if len(word) > 2
            and word
            not in {
                "the",
                "and",
                "for",
                "with",
                "need",
                "borrow",
                "some",
                "this",
                "that",
                "from",
                "want",
                "could",
                "please",
                "a",
                "an",
            }
        ][:8]
        if not words:
            return
        predicates = " OR ".join(
            f"(LOWER(i.name) LIKE :word{n} OR LOWER(i.category) LIKE :word{n} OR LOWER(i.description) LIKE :word{n})"
            for n in range(len(words))
        )
        params: dict[str, str | int] = {"viewer": self._student_id}
        params.update({f"word{n}": f"%{word}%" for n, word in enumerate(words)})
        try:
            async with rx.asession() as session:
                rows = (
                    await session.execute(
                        text(
                            f"SELECT {LISTING_COLUMNS} {LISTING_JOINS} WHERE i.available = true AND i.owner_student_id <> :viewer AND ({predicates}) ORDER BY i.created_at DESC LIMIT 8"
                        ),
                        params,
                    )
                ).all()
            self.need_results = [listing_from_row(row) for row in rows]
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.page_error = (
                "Matching is unavailable right now. Please try again."
            )

    @rx.event
    async def load_browse(self):
        if not await self._guard():
            return rx.redirect("/login")
        try:
            async with rx.asession() as session:
                options = (
                    await session.execute(
                        text(
                            "SELECT 'department' AS kind, department AS value FROM student WHERE department <> '' GROUP BY department UNION ALL SELECT 'location' AS kind, pickup_location AS value FROM item WHERE pickup_location <> '' GROUP BY pickup_location"
                        )
                    )
                ).all()
            self.department_options = [
                "All",
                *sorted(
                    row.value for row in options if row.kind == "department"
                ),
            ]
            self.location_options = [
                "All",
                *sorted(row.value for row in options if row.kind == "location"),
            ]
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.page_error = "Filters couldn't be loaded. Please refresh."
        return CampusState.refresh_browse

    @rx.event
    async def refresh_browse(self):
        if not await self._guard():
            return rx.redirect("/login")
        clauses = ["1 = 1"]
        params: dict[str, str | int | bool] = {"viewer": self._student_id}
        if self.search.strip():
            clauses.append(
                "(LOWER(i.name) LIKE :search OR LOWER(i.description) LIKE :search OR LOWER(i.category) LIKE :search)"
            )
            params["search"] = f"%{self.search.strip().lower()}%"
        if self.category != "All":
            clauses.append("i.category = :category")
            params["category"] = self.category
        if self.availability != "All":
            clauses.append("i.available = :available")
            params["available"] = self.availability == "Available"
        if self.condition_filter != "All":
            clauses.append("i.condition = :condition")
            params["condition"] = self.condition_filter
        if self.department_filter != "All":
            clauses.append("s.department = :department")
            params["department"] = self.department_filter
        if self.year_filter != "All":
            clauses.append("s.year = :year")
            params["year"] = int(self.year_filter)
        if self.location_filter != "All":
            clauses.append("i.pickup_location = :location")
            params["location"] = self.location_filter
        try:
            async with rx.asession() as session:
                rows = (
                    await session.execute(
                        text(
                            f"SELECT {LISTING_COLUMNS} {LISTING_JOINS} WHERE {' AND '.join(clauses)} ORDER BY i.created_at DESC, i.id DESC LIMIT 60"
                        ),
                        params,
                    )
                ).all()
            self.listings = [listing_from_row(row) for row in rows]
            self.page_error = ""
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.page_error = "We couldn't load items. Please try again."

    @rx.event
    def set_search(self, value: str):
        self.search = value[:120]
        return CampusState.refresh_browse

    @rx.event
    def choose_category(self, value: str):
        self.category = value if value in CATEGORIES else "All"
        self.search = ""
        return rx.redirect("/browse")

    @rx.event
    def set_category(self, value: str):
        self.category = value if value in CATEGORIES else "All"
        return CampusState.refresh_browse

    @rx.event
    def set_availability(self, value: str):
        self.availability = (
            value if value in ("All", "Available", "Unavailable") else "All"
        )
        return CampusState.refresh_browse

    @rx.event
    def set_condition_filter(self, value: str):
        self.condition_filter = (
            value if value in ("All", "Like new", "Good", "Fair") else "All"
        )
        return CampusState.refresh_browse

    @rx.event
    def set_department_filter(self, value: str):
        self.department_filter = (
            value if value in self.department_options else "All"
        )
        return CampusState.refresh_browse

    @rx.event
    def set_year_filter(self, value: str):
        self.year_filter = (
            value if value in ("All", "1", "2", "3", "4", "5", "6") else "All"
        )
        return CampusState.refresh_browse

    @rx.event
    def set_location_filter(self, value: str):
        self.location_filter = (
            value if value in self.location_options else "All"
        )
        return CampusState.refresh_browse

    @rx.event
    async def load_item(self):
        if not await self._guard():
            return rx.redirect("/login")
        self.detail_found = False
        self.page_error = ""
        try:
            item_id = int(self.router.page.params.get("item_id", "0"))
            async with rx.asession() as session:
                row = (
                    await session.execute(
                        text(
                            f"SELECT {LISTING_COLUMNS} {LISTING_JOINS} WHERE i.id = :id LIMIT 1"
                        ),
                        {"id": item_id, "viewer": self._student_id},
                    )
                ).first()
            if row:
                self.selected_item = listing_from_row(row)
                self.detail_found = True
        except (ValueError, TypeError):
            pass
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.page_error = "We couldn't load this item. Please try again."

    @rx.event
    async def load_saved(self):
        if not await self._guard():
            return rx.redirect("/login")
        try:
            async with rx.asession() as session:
                rows = (
                    await session.execute(
                        text(
                            f"SELECT {LISTING_COLUMNS} {LISTING_JOINS} WHERE si.id IS NOT NULL ORDER BY si.created_at DESC LIMIT 60"
                        ),
                        {"viewer": self._student_id},
                    )
                ).all()
            self.saved_listings = [listing_from_row(row) for row in rows]
            self.page_error = ""
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.page_error = "We couldn't load saved items. Please try again."

    @rx.event
    async def load_my_items(self):
        if not await self._guard():
            return rx.redirect("/login")
        self.page_error = ""
        try:
            async with rx.asession() as session:
                rows = (
                    await session.execute(
                        text(
                            f"SELECT {LISTING_COLUMNS} {LISTING_JOINS} WHERE i.owner_student_id = :viewer ORDER BY i.created_at DESC, i.id DESC LIMIT 100"
                        ),
                        {"viewer": self._student_id},
                    )
                ).all()
            self.my_items = [listing_from_row(row) for row in rows]
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.page_error = (
                "Your listings couldn't be loaded. Please refresh."
            )

    @rx.event
    def new_listing(self):
        self.listing_form_revision += 1
        self.editing_id = 0
        self.editing_item = {
            "id": 0,
            "name": "",
            "category": "Books",
            "description": "",
            "condition": "Good",
            "available": True,
            "image_path": "",
            "pickup_location": "",
            "preferred_duration_days": 7,
            "owner": "",
            "department": "",
            "year": 1,
            "saved": False,
            "own": True,
        }
        self.draft_image = ""
        self.listing_error = ""
        self.listing_success = ""

    @rx.event
    async def edit_listing(self, item_id: int):
        if not await self._guard():
            return rx.redirect("/login")
        self.listing_error = ""
        self.listing_success = ""
        try:
            async with rx.asession() as session:
                row = (
                    await session.execute(
                        text(
                            f"SELECT {LISTING_COLUMNS} {LISTING_JOINS} WHERE i.id = :id AND i.owner_student_id = :viewer LIMIT 1"
                        ),
                        {"id": item_id, "viewer": self._student_id},
                    )
                ).first()
            if row is None:
                self.listing_error = (
                    "This listing isn't yours or no longer exists."
                )
                return
            self.editing_item = listing_from_row(row)
            self.listing_form_revision += 1
            self.editing_id = item_id
            self.draft_image = self.editing_item["image_path"]
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.listing_error = "Couldn't open this listing. Please try again."

    @rx.event
    async def upload_listing_image(self, files: list[rx.UploadFile]):
        if not await self._guard():
            return rx.redirect("/login")
        self.listing_error = ""
        if len(files) != 1:
            self.listing_error = "Choose one JPG, PNG or WebP image under 5 MB."
            return
        file = files[0]
        try:
            data = await file.read(5 * 1024 * 1024 + 1)
            if len(data) > 5 * 1024 * 1024 or not data:
                self.listing_error = (
                    "Image must be nonempty and smaller than 5 MB."
                )
                return
            signature = data[:16]
            suffix = ""
            if signature.startswith(b"\x89PNG\r\n\x1a\n"):
                suffix = ".png"
            elif signature.startswith(b"\xff\xd8\xff"):
                suffix = ".jpg"
            elif signature.startswith(b"RIFF") and signature[8:12] == b"WEBP":
                suffix = ".webp"
            if not suffix or file.content_type not in (
                "image/png",
                "image/jpeg",
                "image/webp",
            ):
                self.listing_error = (
                    "Only genuine JPG, PNG or WebP images are supported."
                )
                return
            filename = f"listing_{uuid4().hex}{suffix}"
            directory = rx.get_upload_dir()
            directory.mkdir(parents=True, exist_ok=True)
            (directory / filename).write_bytes(data)
            self.draft_image = filename
            self.listing_success = (
                "Photo uploaded. Save the listing to keep it."
            )
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.listing_error = "Couldn't upload the image. Try another file."

    @rx.event
    async def save_listing(self, form_data: dict[str, Any]):
        if not await self._guard():
            return rx.redirect("/login")
        self.listing_error = ""
        self.listing_success = ""
        name = str(form_data.get("name", "")).strip()
        category = str(form_data.get("category", "")).strip()
        description = str(form_data.get("description", "")).strip()
        condition = str(form_data.get("condition", "")).strip()
        location = str(form_data.get("pickup_location", "")).strip()
        raw_duration = str(form_data.get("duration", "")).strip()
        available = str(form_data.get("available", "")) == "true"
        if not 3 <= len(name) <= 120:
            self.listing_error = (
                "Enter an item name between 3 and 120 characters."
            )
        elif category not in CATEGORIES[1:]:
            self.listing_error = "Choose a valid item category."
        elif not 10 <= len(description) <= 2000:
            self.listing_error = "Describe the item in 10–2000 characters."
        elif condition not in ("Like new", "Good", "Fair"):
            self.listing_error = "Choose a valid condition."
        elif not 3 <= len(location) <= 120:
            self.listing_error = (
                "Enter a pickup location between 3 and 120 characters."
            )
        elif not raw_duration.isdecimal() or not 1 <= int(raw_duration) <= 365:
            self.listing_error = "Preferred duration must be 1–365 days."
        elif str(form_data.get("available", "")) not in ("true", "false"):
            self.listing_error = "Choose whether the item is available."
        if self.listing_error:
            return
        params = {
            "name": name,
            "category": category,
            "description": description,
            "condition": condition,
            "location": location,
            "duration": int(raw_duration),
            "available": available,
            "image": self.draft_image,
            "owner": self._student_id,
        }
        try:
            async with rx.asession() as session:
                if self.editing_id:
                    existing = (
                        await session.execute(
                            text(
                                "SELECT available FROM item WHERE id = :id AND owner_student_id = :owner FOR UPDATE"
                            ),
                            {"id": self.editing_id, "owner": self._student_id},
                        )
                    ).first()
                    if existing is None:
                        self.listing_error = (
                            "This listing isn't yours or no longer exists."
                        )
                        return
                    if existing.available != available:
                        busy = (
                            await session.execute(
                                text(
                                    "SELECT id FROM borrow_request WHERE item_id = :id AND status IN ('approved', 'active') LIMIT 1"
                                ),
                                {"id": self.editing_id},
                            )
                        ).first()
                        if busy:
                            self.listing_error = "Availability cannot change while a borrower has an approved or active request."
                            return
                    params["id"] = self.editing_id
                    await session.execute(
                        text(
                            "UPDATE item SET name=:name, category=:category, description=:description, condition=:condition, pickup_location=:location, preferred_duration_days=:duration, available=:available, image_path=:image, updated_at=CURRENT_TIMESTAMP WHERE id=:id AND owner_student_id=:owner"
                        ),
                        params,
                    )
                    message = "Listing updated successfully."
                else:
                    await session.execute(
                        text(
                            "INSERT INTO item (owner_student_id, name, category, description, condition, pickup_location, preferred_duration_days, available, image_path) VALUES (:owner, :name, :category, :description, :condition, :location, :duration, :available, :image)"
                        ),
                        params,
                    )
                    message = "Listing published successfully."
                await session.commit()
            self.listing_success = message
            self.listing_form_revision += 1
            self.editing_id = 0
            self.editing_item = {
                "id": 0,
                "name": "",
                "category": "Books",
                "description": "",
                "condition": "Good",
                "available": True,
                "image_path": "",
                "pickup_location": "",
                "preferred_duration_days": 7,
                "owner": "",
                "department": "",
                "year": 1,
                "saved": False,
                "own": True,
            }
            self.draft_image = ""
            return CampusState.load_my_items
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.listing_error = "Couldn't save this listing. Please try again."

    @rx.event
    async def toggle_item_availability(self, item_id: int):
        if not await self._guard():
            return rx.redirect("/login")
        self.listing_error = ""
        self.listing_success = ""
        try:
            async with rx.asession() as session:
                row = (
                    await session.execute(
                        text(
                            "SELECT available FROM item WHERE id = :id AND owner_student_id = :owner FOR UPDATE"
                        ),
                        {"id": item_id, "owner": self._student_id},
                    )
                ).first()
                if row is None:
                    self.listing_error = (
                        "This listing isn't yours or no longer exists."
                    )
                    return
                busy = (
                    await session.execute(
                        text(
                            "SELECT id FROM borrow_request WHERE item_id = :id AND status IN ('approved', 'active') LIMIT 1"
                        ),
                        {"id": item_id},
                    )
                ).first()
                if busy:
                    self.listing_error = "This item has an approved or active borrow request. Its availability cannot change yet."
                    return
                await session.execute(
                    text(
                        "UPDATE item SET available = :available, updated_at = CURRENT_TIMESTAMP WHERE id = :id AND owner_student_id = :owner"
                    ),
                    {
                        "available": not row.available,
                        "id": item_id,
                        "owner": self._student_id,
                    },
                )
                await session.commit()
            self.listing_success = "Availability updated."
            return CampusState.load_my_items
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.listing_error = (
                "Couldn't change availability. Please try again."
            )

    @rx.event
    async def load_request(self):
        self.request_sent = False
        self.request_error = ""
        self.request_start = ""
        self.request_return = ""
        return CampusState.load_item

    @rx.event
    def set_request_start(self, value: str):
        self.request_start = value

    @rx.event
    def set_request_return(self, value: str):
        self.request_return = value

    @rx.event
    async def submit_request(self, form_data: dict[str, Any]):
        if not await self._guard():
            return rx.redirect("/login")
        self.request_error = ""
        reason = str(form_data.get("reason", "")).strip()
        message = str(form_data.get("message", "")).strip()
        try:
            start = date.fromisoformat(self.request_start)
            end = date.fromisoformat(self.request_return)
        except ValueError:
            self.request_error = "Choose a valid start and return date."
            return
        if start < date.today():
            self.request_error = "Start date cannot be before today."
        elif end < start:
            self.request_error = (
                "Return date must be on or after the start date."
            )
        elif not 10 <= len(reason) <= 500:
            self.request_error = (
                "Explain why you need the item in 10–500 characters."
            )
        elif len(message) > 1000:
            self.request_error = (
                "Optional message must be under 1000 characters."
            )
        if self.request_error:
            return
        try:
            item_id = int(self.router.page.params.get("item_id", "0"))
            async with rx.asession() as session:
                item = (
                    await session.execute(
                        text(
                            "SELECT owner_student_id, available, preferred_duration_days FROM item WHERE id = :id FOR UPDATE"
                        ),
                        {"id": item_id},
                    )
                ).first()
                if item is None:
                    self.request_error = (
                        "This item no longer exists. Browse for another one."
                    )
                    return
                if item.owner_student_id == self._student_id:
                    self.request_error = "You can't request your own item."
                    return
                if not item.available:
                    self.request_error = "This item is no longer available. Browse for another one."
                    return
                if (end - start).days + 1 > item.preferred_duration_days:
                    self.request_error = f"Choose a window of no more than {item.preferred_duration_days} days."
                    return
                duplicate = (
                    await session.execute(
                        text(
                            "SELECT id FROM borrow_request WHERE item_id = :item AND borrower_student_id = :borrower AND status IN ('pending', 'approved', 'active') LIMIT 1"
                        ),
                        {"item": item_id, "borrower": self._student_id},
                    )
                ).first()
                if duplicate:
                    self.request_error = (
                        "You already have an open request for this item."
                    )
                    return
                await session.execute(
                    text(
                        "INSERT INTO borrow_request (item_id, borrower_student_id, lender_student_id, start_date, expected_return_date, reason, message, status) VALUES (:item, :borrower, :lender, :start, :end, :reason, :message, 'pending')"
                    ),
                    {
                        "item": item_id,
                        "borrower": self._student_id,
                        "lender": item.owner_student_id,
                        "start": start,
                        "end": end,
                        "reason": reason,
                        "message": message or None,
                    },
                )
                await session.commit()
            self.request_sent = True
        except (TypeError, ValueError):
            self.request_error = (
                "This item link isn't valid. Browse for another one."
            )
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.request_error = "Couldn't send the request. Please try again."

    @rx.event
    async def toggle_saved(self, item_id: int):
        if not await self._guard():
            return rx.redirect("/login")
        try:
            async with rx.asession() as session:
                item = (
                    await session.execute(
                        text(
                            "SELECT owner_student_id FROM item WHERE id = :id"
                        ),
                        {"id": item_id},
                    )
                ).first()
                if item is None or item.owner_student_id == self._student_id:
                    return
                existing = (
                    await session.execute(
                        text(
                            "SELECT id FROM saved_item WHERE student_id = :student AND item_id = :item"
                        ),
                        {"student": self._student_id, "item": item_id},
                    )
                ).scalar_one_or_none()
                if existing:
                    await session.execute(
                        text(
                            "DELETE FROM saved_item WHERE id = :id AND student_id = :student"
                        ),
                        {"id": existing, "student": self._student_id},
                    )
                else:
                    await session.execute(
                        text(
                            "INSERT INTO saved_item (student_id, item_id) VALUES (:student, :item) ON CONFLICT (student_id, item_id) DO NOTHING"
                        ),
                        {"student": self._student_id, "item": item_id},
                    )
                await session.commit()
            if self.router.url.path.startswith("/saved"):
                return CampusState.load_saved
            if self.router.url.path.startswith("/items/"):
                return CampusState.load_item
            if self.router.url.path.startswith("/browse"):
                return CampusState.refresh_browse
            return CampusState.load_home
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.page_error = (
                "Couldn't update your saved items. Please try again."
            )
