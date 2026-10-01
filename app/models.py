import reflex as rx
from datetime import date, datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
)


class Base(MappedAsDataclass, DeclarativeBase, kw_only=True):
    pass


class Student(Base):
    __tablename__ = "student"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password_hash: Mapped[str]
    name: Mapped[str]
    department: Mapped[str] = mapped_column(default="")
    year: Mapped[int] = mapped_column(default=1)
    is_admin: Mapped[bool] = mapped_column(default=False)
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), init=False
    )

    __table_args__ = (
        CheckConstraint("year >= 1", name="ck_student_year_positive"),
    )


class Item(Base):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    owner_student_id: Mapped[int] = mapped_column(
        ForeignKey("student.id", ondelete="RESTRICT"), index=True
    )
    name: Mapped[str]
    category: Mapped[str] = mapped_column(index=True)
    description: Mapped[str] = mapped_column(default="")
    condition: Mapped[str] = mapped_column(default="Good")
    available: Mapped[bool] = mapped_column(default=True)
    image_path: Mapped[str] = mapped_column(default="")
    preferred_duration_days: Mapped[int] = mapped_column(default=7)
    pickup_location: Mapped[str] = mapped_column(default="")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), init=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        init=False,
    )

    __table_args__ = (
        CheckConstraint(
            "preferred_duration_days >= 1", name="ck_item_duration_positive"
        ),
        Index("ix_item_category_available", "category", "available"),
    )


class BorrowRequest(Base):
    __tablename__ = "borrow_request"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    item_id: Mapped[int] = mapped_column(
        ForeignKey("item.id", ondelete="RESTRICT"), index=True
    )
    borrower_student_id: Mapped[int] = mapped_column(
        ForeignKey("student.id", ondelete="RESTRICT"), index=True
    )
    lender_student_id: Mapped[int] = mapped_column(
        ForeignKey("student.id", ondelete="RESTRICT"), index=True
    )
    start_date: Mapped[date]
    expected_return_date: Mapped[date]
    reason: Mapped[str]
    actual_return_date: Mapped[date | None] = mapped_column(default=None)
    message: Mapped[str | None] = mapped_column(default=None)
    status: Mapped[str] = mapped_column(
        default="pending", server_default="pending"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), init=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        init=False,
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'approved', 'rejected', 'active', 'returned')",
            name="ck_borrow_request_status",
        ),
        CheckConstraint(
            "expected_return_date >= start_date", name="ck_borrow_request_dates"
        ),
        CheckConstraint(
            "borrower_student_id <> lender_student_id",
            name="ck_borrow_request_distinct_students",
        ),
        CheckConstraint(
            "actual_return_date IS NULL OR actual_return_date >= start_date",
            name="ck_borrow_request_actual_return_date",
        ),
        Index(
            "ix_borrow_request_borrower_status", "borrower_student_id", "status"
        ),
        Index("ix_borrow_request_lender_status", "lender_student_id", "status"),
        Index("ix_borrow_request_status_due", "status", "expected_return_date"),
    )


class SavedItem(Base):
    __tablename__ = "saved_item"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    student_id: Mapped[int] = mapped_column(
        ForeignKey("student.id", ondelete="CASCADE"), index=True
    )
    item_id: Mapped[int] = mapped_column(
        ForeignKey("item.id", ondelete="CASCADE"), index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), init=False
    )

    __table_args__ = (
        UniqueConstraint(
            "student_id", "item_id", name="uq_saved_item_student_item"
        ),
    )


class Rating(Base):
    __tablename__ = "rating"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    request_id: Mapped[int] = mapped_column(
        ForeignKey("borrow_request.id", ondelete="RESTRICT"), index=True
    )
    rater_student_id: Mapped[int] = mapped_column(
        ForeignKey("student.id", ondelete="RESTRICT"), index=True
    )
    rated_student_id: Mapped[int] = mapped_column(
        ForeignKey("student.id", ondelete="RESTRICT"), index=True
    )
    score: Mapped[int]
    comment: Mapped[str | None] = mapped_column(default=None)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), init=False
    )

    __table_args__ = (
        CheckConstraint("score BETWEEN 1 AND 5", name="ck_rating_score_range"),
        CheckConstraint(
            "rater_student_id <> rated_student_id",
            name="ck_rating_distinct_students",
        ),
        UniqueConstraint(
            "request_id", "rater_student_id", name="uq_rating_request_rater"
        ),
    )
