from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ..logic.giftcard import get_giftcards
from ..logic.db import get_session
from ..model.wrapper import GiftCard
from ..model.converter import OrmPydanticHelper
from ..enumerators.enums import GiftCardSpentFilter, GiftCardSortField, SortOrderFilter


router = APIRouter(tags=["giftcard"])

@router.get("/", response_model=List[GiftCard])
async def read_giftcards(
    supplier: Optional[str] = Query(None, description="Filter by exact supplier"),
    supplier_search: Optional[str] = Query(None, description="Search supplier substring"),
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    min_amount: Optional[int] = Query(None, description="Minimum gift card amount in cents"),
    max_amount: Optional[int] = Query(None, description="Maximum gift card amount in cents"),
    spent: Optional[GiftCardSpentFilter] = Query(None, description="Filter by spent status"),
    limit: int = Query(50, ge=1, le=100, description="Number of items per page"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    sort_by: Optional[GiftCardSortField] = Query("created_at", description="Field to sort by"),
    sort_order: Optional[SortOrderFilter] = Query("desc", description="Sort order"),
    session: AsyncSession = Depends(get_session),
) -> List[GiftCard]:
    orm_giftcards = await get_giftcards(
        session=session,
        supplier=supplier,
        supplier_search=supplier_search,
        user_id=user_id,
        min_amount=min_amount,
        max_amount=max_amount,
        spent=spent.value if spent else None,
        limit=limit,
        offset=offset,
        sort_by=sort_by.value,
        sort_order=sort_order,
    )

    return [OrmPydanticHelper.orm_to_pydantic(gc, GiftCard) for gc in orm_giftcards]
