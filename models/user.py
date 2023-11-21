from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from config.db import get_metadata, get_engine

users = Table(
    "users",
    get_metadata(),
    Column("id", String(255)),
    Column("name", String(255), nullable=False),
    Column("email", String(255), nullable=False, unique=True),
    Column("password", String(255), nullable=False),
    Column("role", String(255), nullable=False, default="user"),
    Column("created_at", DateTime, nullable=False, default=func.now()),
    Column("updated_at", DateTime, nullable=False, default=func.now()),
)

get_metadata().create_all(get_engine(), tables=[users])