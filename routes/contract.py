from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import json

from config.db import database
from models.contract import contracts
from models.penalty import penalties
from models.streak import streaks
from models.user import users
from schemas.contract import Contract
from schemas.user_auth import UserAuth
from app.deps import get_current_user

from utils.utils import validate_contracts

PROTECTED = [Depends(get_current_user)]

contract_router = APIRouter(
    tags=["Contracts"],
    dependencies=PROTECTED,
    prefix="/api",
)

@contract_router.get("/contracts", response_model=list[Contract])
async def get_contracts(current_user: UserAuth = Depends(get_current_user)):
    query = contracts.select().where(contracts.c.user_id == current_user.id)
    result = await database.fetch_all(query)
    
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))

@contract_router.get("/active-contracts", response_model=list[Contract])
async def get_contracts(current_user: UserAuth = Depends(get_current_user)):
    query = contracts.select().where(
        (contracts.c.status == 1) & 
        (contracts.c.user_id == current_user.id)
    )
    try:
        result = await database.fetch_all(query)
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal Server Error", "detail": str(e)}
        )    

@contract_router.post("/contract")
async def create_contract(contract: Contract, current_user: UserAuth = Depends(get_current_user)):
    
    user_query = users.select().where(users.c.id == current_user.id)
    user = await database.fetch_one(user_query)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "User not found"}
        )
    try:
        query = contracts.insert().values(
            user_id=current_user.id,
            task_id=contract.task_id,
            responsible_name=user.name,
            responsible_email=user.email,
            habit=contract.habit,
            penalty=contract.penalty,
            start=contract.start.strftime("%Y-%m-%d"),
            end=contract.end.strftime("%Y-%m-%d"),
            status=0,
            supervisor_name=contract.supervisor_name,
            supervisor_email=contract.supervisor_email
        )
        
        last_record_id = await database.execute(query)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Contract created successfully", "id": last_record_id})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal Server Error", "detail": str(e)}
        )

@contract_router.put("/contract/{id}")
async def update_contract(id: str, contract_update: Contract, current_user: UserAuth = Depends(get_current_user)):
    
    if not await validate_contracts(id, current_user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Contract not found"})
    
    query_update = (contracts.update().where(
        (contracts.c.id == id) & 
        (contracts.c.user_id == current_user.id)).values(contract_update))
    
    try:    
        result = await database.execute(query_update)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Contract updated successfully"})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal Server Error", "detail": str(e)}
        )

@contract_router.put("/contract/{id}/activate")
async def activate_contract(id: str, current_user: UserAuth = Depends(get_current_user)):

    if not await validate_contracts(id, current_user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Contract not found"})
    
    query_update = contracts.update().where(contracts.c.id == id).values(status=1)
    
    try:
        await database.execute(query_update)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Contract activated successfully"})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal Server Error", "detail": str(e)}
        )    

@contract_router.put("/contract/{id}/deactivate")
async def deactivate_contract(id: str, current_user: UserAuth = Depends(get_current_user)):
    
    if not await validate_contracts(id, current_user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Contract not found"})
    
    query_update = contracts.update().where(
        (contracts.c.id == id) & 
        (contracts.c.user_id == current_user.id)).values(status=0)
    
    try:
        await database.execute(query_update)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Contract activated successfully"})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal Server Error", "detail": str(e)}
        )

@contract_router.delete("/contract/{id}")
async def delete_contract(id: str, current_user: UserAuth = Depends(get_current_user)):
    
    if not await validate_contracts(id, current_user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Contract not found"})
    
    query_delete = contracts.delete().where(
        (contracts.c.id == id) & 
        (contracts.c.user_id == current_user.id))
    
    try:
        await database.execute(query_delete)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Contract deleted successfully"})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal Server Error", "detail": str(e)}
        )

@contract_router.post("/penalty")
async def create_penalty(contract: Contract, current_user: UserAuth = Depends(get_current_user)):
    
    if not await validate_contracts(id, current_user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Contract not found"})
    
    query_insert = penalties.insert().values(contract_id=contract.id, user_id=current_user.id, description=contract.penalty)
    
    try:
        await database.execute(query_insert)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Contract penalty successfully"})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal Server Error", "detail": str(e)}
        )

@contract_router.post("/streak")
async def create_streak(contract: Contract, current_user: UserAuth = Depends(get_current_user)):
    
    if not await validate_contracts(id, current_user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Contract not found"})
    
    query_insert = streaks.insert().values(contract_id=contract.id, user_id=current_user.id)
    
    try:
        await database.execute(query_insert)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Contract streak successfully"})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal Server Error", "detail": str(e)}
        )