from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from config.db import database
from models.user import users

from app.deps import get_current_user

PROTECTED = [Depends(get_current_user)]

user_router = APIRouter(
    prefix="/api",
    dependencies=PROTECTED,
    tags=["Users"]
)

load_dotenv()

@user_router.get("/users", include_in_schema=False)
async def get_users():
    query = users.select()
    list_users = await database.fetch_all(query)
    return JSONResponse(status_code=status.HTTP_200_OK, content=list_users)
