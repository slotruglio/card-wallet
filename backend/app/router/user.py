from fastapi import APIRouter, Depends, Query
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from ..utility.db import get_session
from ..model.wrapper import User
from ..enumerators.enums import SortOrderFilter, UserSortField
router = APIRouter(tags=["users"])

@router.get("/", response_model=List[User])
async def read_users(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    sort_by: UserSortField = Query(UserSortField.created_at),
    sort_order: SortOrderFilter = Query("desc"),
    session: AsyncSession = Depends(get_session)):
    pass

@router.get("/{user_id}", response_model=User)
async def read_user(
    user_id: int,
    include_giftcards: bool = Query(False, description="If true, it will include giftcards"),
    session: AsyncSession = Depends(get_session)):
    pass

@router.post("/", response_model=User)
async def create_user(user: User, session: AsyncSession = Depends(get_session)):
    pass

@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user: User, session: AsyncSession = Depends(get_session)):
    pass

@router.delete("/{user_id}")
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    pass
