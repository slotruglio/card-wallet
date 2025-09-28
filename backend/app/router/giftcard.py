from io import BytesIO
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, UploadFile
from fastapi import exceptions, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ..logic.giftcard import get_giftcards, create_giftcard, save_file, get_file
from ..utility.db import get_session
from ..model.wrapper import GiftCard, FileRead
from ..model.converter import GiftCardOrmPydanticHelper, FileReadOrmPydanticHelper
from ..enumerators.enums import GiftCardSpentFilter, GiftCardSortField, SortOrderFilter


router = APIRouter(tags=["giftcards"])

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
    sort_by: GiftCardSortField = Query("created_at", description="Field to sort by"),
    sort_order: SortOrderFilter = Query("desc", description="Sort order"),
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
    res = []
    for x in orm_giftcards:
        c = await GiftCardOrmPydanticHelper.orm_to_pydantic(x, nested=True)
        res.append(c)
    return res

@router.get("/{giftcard_id}", response_model=GiftCard)
async def read_giftcard(giftcard_id: str):
    pass

@router.get("/{giftcard_id}/download")
async def download_file(giftcard_id: str, session: AsyncSession = Depends(get_session)):
    data = await get_file(session=session, giftcard_id=giftcard_id)
    pyd: FileRead = await FileReadOrmPydanticHelper.orm_to_pydantic(data)
    if pyd is None:
        raise exceptions.HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return StreamingResponse(
        BytesIO(pyd.data),
        media_type=pyd.content_type,
        headers={"Content-Disposition": "attachment; filename={pyd.filename}"}
    )

@router.post("/", response_model=GiftCard)
async def post_giftcard(giftcard: GiftCard, session: AsyncSession = Depends(get_session)):
    data = await create_giftcard(session, giftcard)
    return await GiftCardOrmPydanticHelper.orm_to_pydantic(data, nested=True)

@router.post("/{giftcard_id}/upload", status_code=status.HTTP_202_ACCEPTED, responses={status.HTTP_202_ACCEPTED:{}})
async def upload_giftcard_file(giftcard_id: str, file: UploadFile, session: AsyncSession = Depends(get_session)):
    """
    Upload a PDF or image for a gift card
    """
    if not file.content_type.startswith(("image/", "application/pdf")):
        raise exceptions.HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    await save_file(session, giftcard_id, file)
    return 

@router.patch("/{giftcard_id}/spend")
async def spend_giftcard_amount(giftcard_id: str, spent_amount: int):
    """
    Increment the spent amount for a gift card
    """
    pass


@router.put("/{giftcard_id}", response_model=GiftCard)
async def update_giftcard(giftcard_id: str):
    raise NotImplementedError

@router.delete("/{giftcard_id}")
async def delete_giftcard(giftcard_id: str):
    raise NotImplementedError