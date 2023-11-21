import requests
import os
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from dotenv import load_dotenv
from starlette.responses import JSONResponse

from config.db import database
from models.user import users
from schemas.user_auth import UserAuth
from schemas.user import UserRole

from utils.utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password,
    user_id_is_used
)

auth_router = APIRouter(
    prefix="/api/auth",
    tags=["Auth"]
)

load_dotenv()

@auth_router.post("/signup", summary="Create user account")
async def create_user(data: UserAuth):
    query = users.select().where(users.c.email == data.email)
    user = await database.fetch_one(query)
    
    #Si el usuario ya existe, lanzamos un error
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
        
    #Verificamos que el ID generado no exista en la base de datos
    new_user_id = await user_id_is_used()
        
    user = {
        "id": new_user_id,
        "name": data.name,
        "email": data.email,
        "role": UserRole.user,
        "password": get_hashed_password(data.password),
        
    }
    
    query_insert = users.insert().values(user)
    
    try:
        await database.execute(query_insert)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
    return user
    
@auth_router.post("/login", summary="Login user")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    query_search_user = users.select().where(users.c.email == form_data.username)
    user = await database.fetch_one(query_search_user)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
        
    hashed_pass = user["password"]
    
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
        
    return {
        "access_token": create_access_token(user["email"]),
        "refresh_token": create_refresh_token(user["email"]),
        "user_id": user["id"]
    }
