from datetime import datetime, UTC
from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func
from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, field_validator
from ..utility.dates import force_utc

class BaseClass(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    created_at: AwareDatetime = Field(description="Creation Datetime")
    updated_at: AwareDatetime = Field(description="Last Update Datetime")

    @field_validator("created_at", mode="before")
    def force_utc_created_at(cls, v: datetime) -> datetime:
        return force_utc(v)
    
    @field_validator("updated_at", mode="before")
    def force_utc_updated_at(cls, v: datetime) -> datetime:
        return force_utc(v)

class BaseORM(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.now(tz=UTC),  # lato Python
        server_default=func.now() # lato DB
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.now(tz=UTC),
        onupdate=datetime.now(tz=UTC),
        server_default=func.now()
    )
