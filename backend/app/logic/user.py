from typing import List
from sqlalchemy import select, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession

from ..model.user import UserORM
from ..model.converter import UserOrmPydanticHelper


async def get_users(
    session: AsyncSession,
    limit: int = 50,
    offset: int = 0,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    user_id: str = "",
    user_name: str = ""
) -> List[UserORM]:

    sort_column = getattr(UserORM, sort_by, UserORM.created_at)
    if sort_order.lower() == "desc":
        sort_column = desc(sort_column)
    else:
        sort_column = asc(sort_column)

    stmt = select(UserORM)
    if user_id:
        stmt = stmt.where(UserORM.id == user_id)
    if user_name:
        stmt = stmt.where(UserORM.name == user_name)
    stmt = stmt.order_by(sort_column).limit(limit).offset(offset)
    result = await session.execute(stmt)
    return result.scalars().all()


async def create_user(session: AsyncSession, user) -> UserORM:
    data = UserOrmPydanticHelper.pydantic_to_orm(user)

    session.add(data)
    await session.commit()
    await session.refresh(data)
    return data