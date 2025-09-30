from typing import Type, TypeVar
from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
import uuid

from .wrapper import GiftCard, User, FileRead
from .user import UserORM
from .gift_card import GiftCardORM
from .file import FileReadORM

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
        print(data)
        return orm_model(**data)


class GiftCardOrmPydanticHelper(OrmPydanticHelper):
    @staticmethod
    async def orm_to_pydantic(orm_instance: GiftCardORM, pyd_model = GiftCard, nested: bool = False):
        user = None
        if nested:
            user = await orm_instance.awaitable_attrs.user
            user = await UserOrmPydanticHelper.orm_to_pydantic(user)
        return GiftCard(
            id = orm_instance.id,
            created_at=orm_instance.created_at,
            updated_at=orm_instance.updated_at,
            supplier=orm_instance.supplier,
            amount=orm_instance.amount,
            spent_amount=orm_instance.spent_amount,
            user = user,
            expiration_date=orm_instance.expiration_date
        )
    @staticmethod
    def pydantic_to_orm(pyd_instance: GiftCard):
        return GiftCardORM(
            supplier=pyd_instance.supplier,
            amount=pyd_instance.amount,
            spent_amount=pyd_instance.spent_amount,
            user_id = pyd_instance.user_id,
            expiration_date=pyd_instance.expiration_date
        )
class UserOrmPydanticHelper(OrmPydanticHelper):
    @staticmethod
    async def orm_to_pydantic(orm_instance: UserORM, pyd_model = User, nested: bool = False):
        giftcards = []
        if nested:
            giftcards = await orm_instance.awaitable_attrs.giftcards
            giftcards = [await GiftCardOrmPydanticHelper.orm_to_pydantic(gc) for gc in giftcards]
        return User(
            id = orm_instance.id,
            created_at=orm_instance.created_at,
            updated_at=orm_instance.updated_at,
            name=orm_instance.name,
            giftcards=giftcards
        )
    @staticmethod
    def pydantic_to_orm(pyd_instance: User):
        return UserORM(name=pyd_instance.name)

class FileReadOrmPydanticHelper(OrmPydanticHelper):
    @staticmethod
    async def orm_to_pydantic(orm_instance: FileReadORM, pyd_model= FileRead, nested = True) -> FileRead:
        return FileRead(
            created_at=orm_instance.created_at,
            updated_at=orm_instance.updated_at,
            id = orm_instance.id,
            giftcard_id=orm_instance.giftcard_id,
            filename=orm_instance.filename,
            content_type=orm_instance.content_type,
            data=orm_instance.data
        )
    
    @staticmethod
    def pydantic_to_orm(pyd_instance, orm_model=FileReadORM) -> FileReadORM:
        return FileReadORM(
            giftcard_id=pyd_instance.giftcard_id,
            filename=pyd_instance.filename,
            content_type=pyd_instance.content_type,
            data=pyd_instance.data
        )