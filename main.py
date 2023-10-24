from datetime import datetime
from fastapi import FastAPI
from dotenv import load_dotenv
from routes.contract import contract_router
from routes.todoist import todoist_router
from routes.auth import auth_router
from routes.user import user_router
from fastapi.middleware.cors import CORSMiddleware

from config.db import database
 
app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]    
)

load_dotenv() 

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(contract_router)
app.include_router(todoist_router)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
async def root():
    return f"Bienvenido a CommitGrow API, hora del servidor: {datetime.now()}"
