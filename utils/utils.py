import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
from uuid import uuid4

from config.db import database

from models.contract import contracts
from models.user import users

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
REFRESH_TOKEN_EXPIRE_MINUTES= float(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES"))
ALGORITHM = os.getenv("ALGORITHM")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET_KEY")

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_password(password: str) -> str:
    return password_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)

def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES))
        
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    enconde_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return enconde_jwt

def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=float(REFRESH_TOKEN_EXPIRE_MINUTES))
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encode_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

async def validate_contracts(contract_id, user_id) -> bool:
    query = contracts.select().where(
        (contracts.c.id == contract_id) & 
        (contracts.c.user_id == user_id)
    )
    
    if await database.fetch_one(query) is None:
        return False
    else:
        return True
    
async def user_id_is_used() -> str:
    new_user_id = str(uuid4())
    query_verify_user_id = users.select().where(users.c.id == new_user_id)
    response_verify = await database.fetch_one(query_verify_user_id)
    
    if response_verify is not None:
        await user_id_is_used()
    else:
        return new_user_id