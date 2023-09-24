from fastapi import FastAPI
from routes.user import user
import uvicorn
import os

app = FastAPI()

app.include_router(user, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=os.getenv("PORT", default=5000), log_level="info")