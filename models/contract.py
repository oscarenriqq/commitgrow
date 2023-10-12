from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Date, TEXT
from sqlalchemy.sql import func
from datetime import datetime

from config.db import get_metadata, get_engine

contracts = Table(
    "contracts",
    get_metadata(),
    Column("id", Integer, primary_key=True),
    Column("task_id", String(255), nullable=False),
    Column("responsible_name", String(255), nullable=False),
    Column("responsible_email", String(255), nullable=False),
    Column("habit", String(255), nullable=False),
    Column("description", TEXT, nullable=False),
    Column("penalty", TEXT, nullable=False),
    Column("start", Date, nullable=False),
    Column("end", Date, nullable=False),
    Column("supervisor_name", String(255), nullable=False),
    Column("supervisor_email", String(255), nullable=False),
    Column("status", Integer, nullable=False, default=0),
    Column("created_at", DateTime, nullable=False, default=func.now()),
    Column("updated_at", DateTime, nullable=False, default=func.now()),
)

get_metadata().create_all(get_engine(), tables=[contracts])