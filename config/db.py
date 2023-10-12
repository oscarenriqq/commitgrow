import os
import databases
from sqlalchemy import create_engine, MetaData
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = f"mysql+pymysql://{os.getenv('DBUSER')}:{os.getenv('DBPASS')}@{os.getenv('DBHOST')}:{str(os.getenv('DBPORT'))}/{os.getenv('DBNAME')}"

database = databases.Database(DATABASE_URL)

def get_engine():
    return create_engine(DATABASE_URL)

def get_metadata():
    return MetaData()

def get_conn():
    return get_engine().connect()