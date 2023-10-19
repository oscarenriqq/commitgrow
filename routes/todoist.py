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

task_router = APIRouter()

load_dotenv()

@task_router.get("/redirect")
def redirect(code: str, state: str, current_user: UserAuth=Depends(get_current_user)):
    
    print(current_user)
    
    response = requests.post(
        url="https://todoist.com/oauth/access_token", 
        data= {
            "client_id": os.getenv('TODOIST_CLIENT_ID'),
            "client_secret": os.getenv('TODOIST_CLIENT_SECRET'),
            "code": code
        }
    )
    
    user_todoist_data = {
        "user_id": current_user.id,
        "secret_string": state,
        "access_token": data["access_token"],
    }
    
    data = response.json()
    query = users_todoist_credentials.insert().values(user_todoist_data)
    result = database.execute(query)

    return JSONResponse(content={ "message": "success" }, status_code=status.HTTP_200_OK)

@task_router.get("/todoist-tasks")
def get_tasks():
    return JSONResponse(status_code=200, content=todoist.get_todoist_tasks())

@task_router.get("/todoist-task/{id}")
def get_tasks(id: str):
    return JSONResponse(status_code=200, content=todoist.get_todoist_task(task_id=id))