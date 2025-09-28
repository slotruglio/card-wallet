from typing import Type, TypeVar
from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
import uuid

ORM = TypeVar("ORM", bound=DeclarativeBase)
Pyd = TypeVar("Pyd", bound=BaseModel)


class OrmPydanticHelper:
    @staticmethod
    async def orm_to_pydantic(
        orm_instance: ORM, pyd_model: Type[Pyd], nested: bool = True
    ) -> Pyd:
        """
        Convert ORM -> Pydantic (async-aware)
        If nested=True, also converts relationships if they are Pydantic-compatible.
        Works with async lazy-loaded relationships via AsyncAttrs.
        """
        data = {}
        for field in pyd_model.model_fields:
            if hasattr(orm_instance, field):
                value = getattr(orm_instance, field)

                # handle async lazy-loaded attributes
                if isinstance(orm_instance, AsyncAttrs):
                    awaitable_attrs = orm_instance.awaitable_attrs
                    attr = getattr(awaitable_attrs, field, None)
                    if attr is not None:
                        value = await attr

                # convert UUID to str
                if isinstance(value, uuid.UUID):
                    value = str(value)

                # recursively convert nested ORM objects
                elif nested and hasattr(value, "__iter__") and not isinstance(value, (str, bytes, dict)):
                    value = [await OrmPydanticHelper.orm_to_pydantic(v, pyd_model.model_fields[field].annotation) for v in value]

                elif nested and hasattr(value, "__table__"):
                    value = await OrmPydanticHelper.orm_to_pydantic(value, pyd_model.model_fields[field].annotation)

                data[field] = value

        return pyd_model(**data)

    @staticmethod
    def pydantic_to_orm(pyd_instance: Pyd, orm_model: Type[ORM]) -> ORM:
        """
        Convert Pydantic -> ORM
        Handles UUID conversion automatically
        """
        data = pyd_instance.model_dump(exclude_unset=True)
        if "id" in data and isinstance(data["id"], str):
            try:
                data["id"] = uuid.UUID(data["id"])
            except ValueError:
                pass  # keep original if not a valid UUID
        return orm_model(**data)
