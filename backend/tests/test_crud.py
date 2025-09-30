import pytest
from app.model.converter import OrmPydanticHelper
from app.model.wrapper import User

@pytest.mark.asyncio
async def test_orm_to_pydantic(session, sample_user):
    pyd_user = await OrmPydanticHelper.orm_to_pydantic(sample_user, User)
    assert pyd_user.name == "John Doe"
