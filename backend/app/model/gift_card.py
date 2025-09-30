from __future__ import annotations  # Needed for Python 3.11+ forward references

from datetime import datetime
from decimal import Decimal
from typing import Optional
import uuid
from sqlalchemy import TIMESTAMP, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pydantic import AwareDatetime, Field, computed_field, field_validator

from ..utility.dates import force_utc
from ..utility.currency import currency_to_int
from .base import BaseClass, BaseORM

class GiftCard(BaseClass):
    id: Optional[uuid.UUID] = Field(default=None, description="Gift Card ID", examples=["dc103a36-7167-4d91-9107-46ebd7e2ef22", "fa4ca904-0bc4-4fee-ad6f-5a89db7a3281"]) 
    supplier: str = Field(description="Gift Card Producer", examples=["Amazon", "Q8"])
    amount: Decimal = Field(description="Amount in EURO of the gift card. This number is the value x100 to be int", decimal_places=2, examples=[1230.00, 120.00])
    spent_amount: Decimal = Field(default=0.00, description="Spent Amount in EURO of the gift card. This number is the value x100 to be int", decimal_places=2, examples=[1230.00, 120.00])
    user: Optional["User"] = Field(default=None, description="User who owns the giftcard")
    file: Optional[bytes] = Field(default=None, description="GiftCard as bytes. can be an image or a pdf")
    expiration_date: Optional[AwareDatetime] = Field(default=None, description="Expiration date")

    @field_validator("expiration_date", mode="before")
    def force_utc_expiration_date(cls, v: datetime) -> datetime:
        return force_utc(v)

    @computed_field(return_type=str, description="user id", examples=["dc103a36-7167-4d91-9107-46ebd7e2ef22", "fa4ca904-0bc4-4fee-ad6f-5a89db7a3281"])
    @property
    def user_id(self) -> str:
        if self.user is not None:
            return str(self.user.id)
        return ""

    @computed_field(return_type=int,description="Amount from decimal to int", examples=[123000, 12000])
    @property
    def amount_as_cents(self) -> Decimal:
        return currency_to_int(self.amount)


    @computed_field(return_type=int, description="Spent Amount from decimal to int", examples=[123000, 12000])
    @property
    def spent_amounts_as_cents(self) -> Decimal:
        return currency_to_int(self.spent_amount)

    @computed_field(return_type=Decimal, description="Available Amount in EURO of the gift card. This number is the value x100 to be int", examples=[123000, 12000])
    @property
    def available_amount(self) -> Decimal:
        return self.amount - self.spent_amount

class GiftCardORM(BaseORM):
    __tablename__ = "giftcard"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    supplier: Mapped[str] = mapped_column(nullable=False)
    amount: Mapped[int] = mapped_column(nullable=False)
    spent_amount: Mapped[int] = mapped_column(default=0)
    expiration_date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)

    user_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("user.id", ondelete="SET NULL"),
        nullable=True
    )
    user: Mapped["UserORM"] = relationship(
        "UserORM",
        back_populates="giftcards",
        lazy="selectin"
    )

    file_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("file.id", ondelete="SET NULL"),
        nullable=True
    )
    file = relationship(
        "FileReadORM",
        uselist=False,  # important: one-to-one
        cascade="all, delete-orphan",
        single_parent=True
    )
