#https://todoist.com/oauth/authorize?client_id=8ded4bfa03754acab19effa822a484c0&scope=data:read&state=secretstring

from fastapi import FastAPI
from routes.user import user

app = FastAPI()

app.include_router(user, prefix="/api")