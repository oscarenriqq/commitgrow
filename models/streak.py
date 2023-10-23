from sqlalchemy import Table, Column
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Date, TEXT
from datetime import datetime

from config.db import get_metadata, get_engine

streaks = Table(
    "streaks",
    get_metadata(),
    Column("id", Integer, primary_key=True),
    Column("user_id", String(255), nullable=False),
    Column("contract_id", Integer, nullable=False),
    Column("created_at", DateTime, nullable=False, default=func.now()),
    Column("updated_at", DateTime, nullable=False, default=func.now()),
)

get_metadata().create_all(get_engine(), tables=[streaks])