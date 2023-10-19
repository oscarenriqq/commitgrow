import requests
import os
from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from utils import todoist

from models.users_todoist_credentials import users_todoist_credentials
from schemas.user_auth import UserAuth
from config.db import database
from app.deps import get_current_user

todoist_router = APIRouter()

load_dotenv()

@todoist_router.post("/authorize")
async def authorize(secret_string: str, current_user: UserAuth = Depends(get_current_user)):
    
    query = users_todoist_credentials.select().where(users_todoist_credentials.c.secret_string == secret_string)
    result = await database.execute(query)
    
    users_todoist_credentials_data = { "user_id": current_user.id, "secret_string": secret_string, "access_token": "" }
    
    if result is None:
        query = users_todoist_credentials.insert().values(users_todoist_credentials_data)
        await database.execute(query)
    else:
        query = users_todoist_credentials.update().where(users_todoist_credentials.c.secret_string == secret_string).values(users_todoist_credentials_data)
        await database.execute(query)
            
    return JSONResponse(content={ "url": "{}{}".format(os.getenv('TODOIST_AUTH_URL'),secret_string) }, status_code=status.HTTP_200_OK)

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
    
    query_user = users_todoist_credentials.select().where(users_todoist_credentials.c.secret_string == state)
    user = await database.fetch_one(query_user)
    
    user_todoist_data = {
        "access_token": todoist_auth_data['access_token'],
    }
    
    query = users_todoist_credentials.update().where(users_todoist_credentials.c.user_id == user.id).values(user_todoist_data)
    await database.execute(query)

    return JSONResponse(content={ "message": "Todoist Authentication Complete." }, status_code=status.HTTP_200_OK)

@todoist_router.get("/todoist-tasks")
def get_tasks():
    return JSONResponse(status_code=200, content=todoist.get_todoist_tasks())

@todoist_router.get("/todoist-task/{id}")
def get_tasks(id: str):
    return JSONResponse(status_code=200, content=todoist.get_todoist_task(task_id=id))