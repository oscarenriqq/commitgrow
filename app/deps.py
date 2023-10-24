import os
from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
from jose import jwt
from pydantic import ValidationError, BaseModel

from config.db import database
from models.user import users

from schemas.user_auth import UserAuth

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login",
    scheme_name="JWT"
)

load_dotenv()

class TokenPayload(BaseModel):
    sub: Union[str, Any]
    exp: int
    
class SystemUser(BaseModel):
    id: str
    name: str
    email: str
    password: str
    
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

async def get_current_user(token: str = Depends(reuseable_oauth)) -> UserAuth:
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError, Exception) as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials \n {}".format(str(e)),
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    query_search_user = users.select().where(users.c.email == token_data.sub)
    user = await database.fetch_one(query_search_user)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    
    return UserAuth(**user)