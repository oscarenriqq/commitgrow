from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Boolean
from config.db import get_metadata, get_engine
import datetime

users = Table(
    "users",
    get_metadata(),
    Column("id", Integer, primary_key=True),
    Column("name", String(255), nullable=False),
    Column("email", String(255), nullable=False, unique=True),
    Column("password", String(255), nullable=False),
    Column("secret_string", String(255), nullable=False),
    Column("todoist_access_token", String(255), nullable=True),
    Column("created_at", DateTime, nullable=False, default=datetime.datetime.now()),
    Column("updated_at", DateTime, nullable=False, default=datetime.datetime.now()),
)

get_metadata().create_all(get_engine(), tables=[users])