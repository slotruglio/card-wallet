from datetime import datetime, UTC
from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func
from pydantic import AwareDatetime, BaseModel, ConfigDict, Field

class BaseClass(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    created_at: AwareDatetime = Field(description="Creation Datetime")
    updated_at: AwareDatetime = Field(description="Last Update Datetime")

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
