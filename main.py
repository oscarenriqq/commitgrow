from fastapi import FastAPI
from routes.user import user
from routes.auth import auth

app = FastAPI()

app.include_router(user, prefix="/api")
app.include_router(auth, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Hello World"}
