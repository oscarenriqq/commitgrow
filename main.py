from fastapi import FastAPI
from routes.user import user
import uvicorn
import os

app = FastAPI()

app.include_router(user, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Hello World"}
