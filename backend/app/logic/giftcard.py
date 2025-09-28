from typing import List, Optional
from fastapi import UploadFile
from sqlalchemy import select, and_, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession

from ..model.file import FileReadORM
from ..model.gift_card import GiftCardORM
from ..model.converter import GiftCardOrmPydanticHelper


async def get_giftcards(
    session: AsyncSession,
    supplier: Optional[str] = None,
    supplier_search: Optional[str] = None,
    user_id: Optional[int] = None,
    min_amount: Optional[int] = None,
    max_amount: Optional[int] = None,
    spent: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    giftcard_id: str = ""
) -> List[GiftCardORM]:

    filters = []

    if giftcard_id:
        filters.append(GiftCardORM.id == giftcard_id)
    if supplier:
        filters.append(GiftCardORM.supplier == supplier)
    if supplier_search:
        filters.append(GiftCardORM.supplier.ilike(f"%{supplier_search}%"))
    if user_id:
        filters.append(GiftCardORM.user_id == user_id)
    if min_amount is not None:
        filters.append(GiftCardORM.amount >= min_amount)
    if max_amount is not None:
        filters.append(GiftCardORM.amount <= max_amount)
    if spent:
        if spent == "unused":
            filters.append(GiftCardORM.spent_amount == 0)
        elif spent == "partial":
            filters.append(
                and_(
                    GiftCardORM.spent_amount > 0,
                    GiftCardORM.spent_amount < GiftCardORM.amount,
                )
            )
        elif spent == "full":
            filters.append(GiftCardORM.spent_amount >= GiftCardORM.amount)

    sort_column = getattr(GiftCardORM, sort_by, GiftCardORM.created_at)
    if sort_order.lower() == "desc":
        sort_column = desc(sort_column)
    else:
        sort_column = asc(sort_column)

    stmt = select(GiftCardORM).where(*filters).order_by(sort_column).limit(limit).offset(offset)
    result = await session.execute(stmt)
    return result.scalars().all()

async def create_giftcard(session: AsyncSession, giftcard) -> GiftCardORM:
    data = GiftCardOrmPydanticHelper.pydantic_to_orm(giftcard)
    session.add(data)
    await session.commit()
    await session.refresh(data)
    return data

async def save_file(session: AsyncSession, giftcard_id: str, file: UploadFile):
    contents = await file.read()  # read entire file into memory

    fl = FileReadORM(
        giftcard_id=giftcard_id,
        data= contents,
        filename = file.filename,
        content_type = file.content_type
    )
    session.add(fl)
    await session.commit()
    
async def get_file(session: AsyncSession, giftcard_id: str) -> FileReadORM:
    stmt = select(FileReadORM).where(FileReadORM.giftcard_id == giftcard_id)
    result = await session.execute(stmt)
    return result.scalars().first()
