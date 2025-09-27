from app.model.converter import OrmPydanticHelper
from app.model.user import UserORM, User

def test_orm_to_pydantic(db_session, sample_user):
    pyd_user = OrmPydanticHelper.orm_to_pydantic(sample_user, User)
    assert pyd_user.name == "John Doe"
