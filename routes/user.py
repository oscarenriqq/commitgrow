from fastapi import APIRouter
from starlette.status import HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR
from starlette.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os
import random

from config.db import get_conn
from models.user import users

user = APIRouter()

load_dotenv()

key = Fernet.generate_key()
f = Fernet(key)

@user.post("/user")
def create_user(name: str, email: str, password: str):
    try:        
        
        long_string = str(random.getrandbits(128))
        
        conn = get_conn()
        conn.execute(users.insert().values(name=name, email=email, password=f.encrypt(password.encode('utf-8')), secret_string=long_string))
        conn.commit()
        conn.close()
    except SQLAlchemyError as e:
        return JSONResponse(content=str(e.orig.args[1]), status_code=HTTP_500_INTERNAL_SERVER_ERROR)
    return JSONResponse(content=f"{os.getenv('TODOIST_AUTH_URL')}{long_string}", status_code=HTTP_201_CREATED)