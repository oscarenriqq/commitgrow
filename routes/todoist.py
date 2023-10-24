import requests
import os
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from utils import todoist

from models.users_todoist_credentials import users_todoist_credentials
from schemas.user_auth import UserAuth
from schemas.todoist import Todoist
from config.db import database
from app.deps import get_current_user

todoist_router = APIRouter(tags=["Todoist Integration"], prefix="/api/todoist")

load_dotenv()

@todoist_router.post("/authorize")
async def authorize(todoist: Todoist, current_user: UserAuth = Depends(get_current_user)):
    
    query = users_todoist_credentials.select().where(users_todoist_credentials.c.user_id == current_user.id)
    result = await database.fetch_one(query)
    
    if result is None:
        users_todoist_credentials_data = { "user_id": current_user.id, "secret_string": todoist.secret_string, "access_token": "" }
        query_insert = users_todoist_credentials.insert().values(users_todoist_credentials_data)
        await database.execute(query_insert)
    else:
        query_update = users_todoist_credentials.update().where(users_todoist_credentials.c.user_id == current_user.id).values(secret_string=todoist.secret_string)
        await database.execute(query_update)
            
    return JSONResponse(content={ "url": "{}{}".format(os.getenv('TODOIST_AUTH_URL'), todoist.secret_string) }, status_code=status.HTTP_200_OK)

@todoist_router.get("/redirect")
async def redirect(code: str, state: str):
    
    response = requests.post(
        url="https://todoist.com/oauth/access_token", 
        data= {
            "client_id": os.getenv('TODOIST_CLIENT_ID'),
            "client_secret": os.getenv('TODOIST_CLIENT_SECRET'),
            "code": code
        }
    )
    
    todoist_auth_data = response.json()

    if "error" in todoist_auth_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={ "message": "Todoist Authentication Failed." })
        
    query_user = users_todoist_credentials.select().where(users_todoist_credentials.c.secret_string == state)
    user_todoist_data = await database.fetch_one(query_user)
    
    query = users_todoist_credentials.update().where(users_todoist_credentials.c.user_id == user_todoist_data.user_id).values(access_token=str(todoist_auth_data['access_token']))
    await database.execute(query)

    return JSONResponse(content={ "message": "Todoist Authentication Complete." }, status_code=status.HTTP_200_OK)

@todoist_router.get("/verify-integration")
async def verify_integration(current_user: UserAuth = Depends(get_current_user)):
    query_user = users_todoist_credentials.select().where(users_todoist_credentials.c.user_id == current_user.id)
    user_todoist_data = await database.fetch_one(query_user)
    
    if user_todoist_data is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={ "message": "User not found." })
    
    if user_todoist_data.access_token == "":
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={ "message": "Integration not activated." })
    
    return JSONResponse(status_code=status.HTTP_200_OK, content={ "message": "Integration activated." })

@todoist_router.get("/todoist-tasks")
def get_tasks(current_user: UserAuth = Depends(get_current_user)):
    return JSONResponse(status_code=status.HTTP_200_OK, content=todoist.get_todoist_tasks())

@todoist_router.get("/todoist-task/{id}")
def get_tasks(id: str, current_user: UserAuth = Depends(get_current_user)):
    return JSONResponse(status_code=status.HTTP_200_OK, content=todoist.get_todoist_task(task_id=id))

@todoist_router.delete("/deactivate-integration")
async def deactivate_integration(current_user: UserAuth = Depends(get_current_user)):
    query_user = users_todoist_credentials.select().where(users_todoist_credentials.c.user_id == current_user.id)
    user_todoist_data = await database.fetch_one(query_user)
    
    if user_todoist_data is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={ "message": "User not found." })
    
    try:
        query_delete = users_todoist_credentials.delete().where(users_todoist_credentials.c.user_id == current_user.id)
        await database.execute(query_delete)
        
        return JSONResponse(status_code=status.HTTP_200_OK, content={ "message": "Integration deactivated successfully." })
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_201_CREATED, detail={ "message": "Internal Server Error.", "detail": str(e) })
    
