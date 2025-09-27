from sqlalchemy.dialects import postgresql
from sqlalchemy.schema import CreateTable
from ..model.base import BaseORM
from ..model.gift_card import GiftCardORM
from ..model.user import UserORM


with open("schema.sql", "w") as f:
    for table in BaseORM.metadata.sorted_tables:
        ddl = str(CreateTable(table).compile(dialect=postgresql.dialect()))
        f.write(ddl + ";\n")