from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from dotenv import load_dotenv
from sqlalchemy import select

from config.db import database
from models.user import users
from models.users_todoist_credentials import users_todoist_credentials

from app.deps import get_current_user

user_router = APIRouter(
    prefix="/api",
    tags=["Users"]
)

load_dotenv()

@user_router.get("/users")
async def get_users(current_user=Depends(get_current_user)):
    query = (
        select([users.c.id, users.c.name, users.c.email, users.c.role, users_todoist_credentials.c.access_token])
        .select_from(users.join(users_todoist_credentials, users.c.id == users_todoist_credentials.c.user_id))
        .with_only_columns(users.c.id, users.c.name, users.c.email, users.c.role, users_todoist_credentials.c.access_token)
    )
    users_list = await database.fetch_all(query)
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(users_list))

@user_router.get("/user")
async def get_users(current_user=Depends(get_current_user)):
    user = await database.fetch_one(users.select().with_only_columns(users.c.id, users.c.name, users.c.email).where(users.c.id == current_user.id))
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(user))
