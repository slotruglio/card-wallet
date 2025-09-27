from __future__ import annotations  # Needed for Python 3.11+ forward references

from datetime import datetime
from typing import Optional
import uuid
from sqlalchemy import TIMESTAMP, UUID, ForeignKey, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pydantic import AwareDatetime, Field, computed_field, field_validator

from ..utility.dates import force_utc

from .base import BaseClass, BaseORM

def int_to_currency(a: int) -> float:
    return a / 100

def currency_to_int(a: float) -> int:
    return round(a * 100) 

class GiftCard(BaseClass):
    id: uuid.UUID = Field(description="Gift Card ID", examples=["dc103a36-7167-4d91-9107-46ebd7e2ef22", "fa4ca904-0bc4-4fee-ad6f-5a89db7a3281"]) 
    supplier: str = Field(description="Gift Card Producer", examples=["Amazon", "Q8"])
    amount: int = Field(description="Amount in EURO of the gift card. This number is the value x100 to be int", examples=[123000, 12000])
    spent_amount: int = Field(description="Spent Amount in EURO of the gift card. This number is the value x100 to be int", examples=[123000, 12000])
    user: Optional["User"] = Field(default=None, description="User who owns the giftcard")
    file: Optional[bytes] = Field(default=None, description="GiftCard as bytes. can be an image or a pdf")
    expiration_date: Optional[AwareDatetime] = Field(default=None, description="Expiration date")

    @field_validator("expiration_date", mode="before")
    def force_utc_expiration_date(cls, v: datetime) -> datetime:
        return force_utc(v)

    @computed_field(return_type=float,description="Amount in EURO of the gift card", examples=[1230.00, 120.00])
    @property
    def currency_amount(self) -> float:
        return int_to_currency(self.amount)


    @computed_field(return_type=float, description="Spent Amount in EURO of the gift card", examples=[1230.00, 120.00])
    @property
    def currency_spent_amount(self) -> float:
        return int_to_currency(self.spent_amount)

    @computed_field(return_type=int, description="Available Amount in EURO of the gift card. This number is the value x100 to be int", examples=[123000, 12000])
    @property
    def available_amount(self) -> int:
        return self.amount - self.spent_amount
    
    @computed_field(return_type=float, description="Available Amount in EURO of the gift card", examples=[1230.00, 120.00])
    @property
    def currency_available_amount(self) -> float:
        return int_to_currency(self.available_amount)

class GiftCardORM(BaseORM):
    __tablename__ = "giftcard"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    supplier: Mapped[str] = mapped_column(nullable=False)
    amount: Mapped[int] = mapped_column(nullable=False)
    spent_amount: Mapped[int] = mapped_column(default=0)
    expiration_date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("user.id", ondelete="SET NULL"),
        nullable=True
    )
    user: Mapped["UserORM"] = relationship(
        "UserORM",
        back_populates="giftcards"
    )

    file: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
