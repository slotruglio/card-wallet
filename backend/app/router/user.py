from fastapi import APIRouter, Depends, Query
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from ..utility.db import get_session
from ..model.wrapper import User
from ..enumerators.enums import SortOrderFilter, UserSortField
from ..logic import user as bl
from ..model.converter import UserOrmPydanticHelper
from fastapi import status
from fastapi import exceptions
router = APIRouter(tags=["users"])

@router.get("/", response_model=List[User])
async def read_users(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    sort_by: UserSortField = Query(UserSortField.created_at),
    sort_order: SortOrderFilter = Query("desc"),
    session: AsyncSession = Depends(get_session)):
    data = await bl.get_users(session=session, limit=limit, offset=offset, sort_by=sort_by.value, sort_order=sort_order.value)
    
    res = []
    for x in data:
        c = await UserOrmPydanticHelper.orm_to_pydantic(x)
        res.append(c)
    return res


@router.get("/{user_id}", response_model=User)
async def read_user(
    user_id: str,
    include_giftcards: bool = Query(False, description="If true, it will include giftcards"),
    session: AsyncSession = Depends(get_session)):
    data = await bl.get_users(session, user_id=user_id, limit=1)
    if len(data) == 0:
        raise exceptions.HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return await UserOrmPydanticHelper.orm_to_pydantic(data[0], nested=include_giftcards)

@router.post("/", response_model=User)
async def post_user(user: User, session: AsyncSession = Depends(get_session)):
    try:
        data = await bl.create_user(session, user)
    except IntegrityError:
        raise exceptions.HTTPException(status_code=status.HTTP_409_CONFLICT)
    as_pyd = await UserOrmPydanticHelper.orm_to_pydantic(data)
    return as_pyd

@router.put("/{user_id}", response_model=User)
async def update_user(user_id: str, user: User, session: AsyncSession = Depends(get_session)):
    raise NotImplementedError

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, session: AsyncSession = Depends(get_session)):
    await bl.delete_user(session=session, user_id=user_id)
