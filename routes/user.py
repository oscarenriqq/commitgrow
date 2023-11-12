from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from dotenv import load_dotenv

from config.db import database
from models.user import users

from app.deps import get_current_user

user_router = APIRouter(
    prefix="/api",
    tags=["Users"]
)

load_dotenv()

@user_router.get("/user")
async def get_users(current_user=Depends(get_current_user)):
    user = await database.fetch_one(users.select().with_only_columns(users.c.id, users.c.name, users.c.email).where(users.c.id == current_user.id))
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(user))
