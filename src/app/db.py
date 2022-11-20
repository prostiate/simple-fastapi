import os

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    MetaData,
    String,
    Table,
    create_engine
)
from sqlalchemy.sql import func
from databases import Database

DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()

customer = Table(
    "customer",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("customer_number", Integer),
    Column("name", String(50)),
    Column("created_date", DateTime, default=func.now(), nullable=False),
)

account = Table(
    "account",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("account_number", Integer),
    Column("customer_number", Integer),
    Column("balance", Integer),
    Column("created_date", DateTime, default=func.now(), nullable=False),
)

# databases query builder
database = Database(DATABASE_URL)
