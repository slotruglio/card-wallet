from __future__ import annotations  # Needed for Python 3.11+ forward references

from typing import Optional
import uuid
from sqlalchemy import UUID, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column

from pydantic import Field


from .base import BaseClass, BaseORM


class FileRead(BaseClass):
    id: Optional[uuid.UUID] = Field(default=None, description="File ID", examples=["dc103a36-7167-4d91-9107-46ebd7e2ef22", "fa4ca904-0bc4-4fee-ad6f-5a89db7a3281"]) 
    giftcard_id: uuid.UUID = Field(description="Giftcard to which is related", examples=["dc103a36-7167-4d91-9107-46ebd7e2ef22", "fa4ca904-0bc4-4fee-ad6f-5a89db7a3281"])
    filename: str = Field(description="Filename", examples=["gift.pdf", "image.png"])
    content_type: str = Field(description="Content type", examples=["pdf", "png"])
    data: bytes = Field(description="Content bytes")


class FileReadORM(BaseORM):
    __tablename__ = "file"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    giftcard_id: Mapped[uuid.UUID] = mapped_column(UUID, unique=True)

    filename: Mapped[str] = mapped_column(nullable=False)
    content_type: Mapped[str] = mapped_column(nullable=False)
    data: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
