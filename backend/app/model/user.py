from __future__ import annotations
from typing import List, Optional
import uuid

from sqlalchemy import UUID  # Needed for Python 3.11+ forward references


from .base import BaseClass, BaseORM
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pydantic import Field

class User(BaseClass):
    id: Optional[uuid.UUID] = Field(default=None, description="User ID", examples=["dc103a36-7167-4d91-9107-46ebd7e2ef22", "fa4ca904-0bc4-4fee-ad6f-5a89db7a3281"]) 
    name: str = Field(description="User Name", examples=["john", "mario"])
    giftcards: list["GiftCard"] = Field(default=list(), description="User's giftcards")


class UserORM(BaseORM):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(unique=True)

    # Lista giftcard → relazione inversa
    giftcards: Mapped[List["GiftCardORM"]] = relationship(
        "GiftCardORM",
        back_populates="user",
        passive_deletes=True,  # evita cancellazioni in cascata
        lazy="selectin"
    )