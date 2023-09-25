from fastapi import APIRouter
from dotenv import load_dotenv
import requests
import os

auth = APIRouter()

load_dotenv()

@auth.get("/redirect")
def redirect(code: str, state: str):
    
    response = requests.post(
        "https://todoist.com/oauth/access_token", 
        params= {
            "client_id": os.getenv('TODOIST_CLIENT_ID'),
            "client_secret": os.getenv('TODOIST_CLIENT_SECRET'),
            "code": code
        }
    )
    
    data = response.json()
    
    return data
