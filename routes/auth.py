from fastapi import APIRouter
from dotenv import load_dotenv
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK
import requests
import os

from config.db import get_conn
from models.user import users

auth = APIRouter()

load_dotenv()

@auth.get("/redirect")
def redirect(code: str, state: str):
    
    response = requests.post(
        url="https://todoist.com/oauth/access_token", 
        data= {
            "client_id": os.getenv('TODOIST_CLIENT_ID'),
            "client_secret": os.getenv('TODOIST_CLIENT_SECRET'),
            "code": code
        }
    )
    
    data = response.json()
    conn = get_conn()
    conn.execute(users.update().where(users.c.secret_string == state).values(todoist_access_token=data['access_token']))
    conn.commit()

    return JSONResponse(content={ "message": "success" }, status_code=HTTP_200_OK)