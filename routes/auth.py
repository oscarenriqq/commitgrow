from fastapi import APIRouter

auth = APIRouter()

@auth.get("/redirect")
def redirect(code: str, state: str):
    return {"code": code, "state": state}