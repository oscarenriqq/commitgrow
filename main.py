from datetime import datetime
from fastapi import FastAPI
from dotenv import load_dotenv
from routes.contract import contract_route
from routes.todoist import task_router
from routes.auth import auth_router
from routes.user import user_route

from config.db import database
 
app = FastAPI()

load_dotenv() 

app.include_router(user_route)
app.include_router(auth_router)
app.include_router(contract_route)
app.include_router(task_router)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
async def root():
    return f"Bienvenido a CommitGrow - {datetime.now()} - UTC {datetime.utcnow()}"
