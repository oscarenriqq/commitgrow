import os
import random
from fastapi import APIRouter, Depends
from starlette.status import HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR
from starlette.requests import Request
from sqlalchemy.exc import SQLAlchemyError
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from typing import Any, Annotated

from config.db import database
from models.user import users
from schemas.user_auth import UserAuth

from app.deps import get_current_user

PROTECTED = [Depends(get_current_user)]

user_route = APIRouter(
    prefix="/api",
    dependencies=PROTECTED
)

load_dotenv()

@user_route.get("/users")
async def get_users():
    query = users.select()
    return await database.fetch_all(query)
