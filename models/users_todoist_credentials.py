from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String, DateTime
from sqlalchemy.sql import func
from config.db import get_metadata, get_engine

users_todoist_credentials = Table(
    "users_todoist_credentials",
    get_metadata(),
    Column("user_id", String(255), nullable=False, primary_key=True),
    Column("access_token", String(255), nullable=False, default=""),
    Column("secret_string", String(255), nullable=False, default=""),
    Column("created_at", DateTime, nullable=False, default=func.now()),
    Column("updated_at", DateTime, nullable=False, default=func.now())
)

get_metadata().create_all(get_engine(), tables=[users_todoist_credentials])