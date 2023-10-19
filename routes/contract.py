import os
import json
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from fastapi import Request

from config.db import database
from models.contract import contracts
from models.penalty import penalties
from models.streak import streaks
from schemas.contract import Contract

from services.serializer import serialize_date

contract_route = APIRouter()

@contract_route.get("/contracts", response_model=list[Contract])
async def get_contracts():
    query = contracts.select()
    return await database.fetch_all(query)

@contract_route.get("/active-contracts", response_model=list[Contract])
async def get_contracts():
    query = contracts.select().where(contracts.c.status == 1)
    return await database.fetch_all(query)

@contract_route.post("/contract")
async def create_contract(contract: Contract):
    query = contracts.insert().values(
        task_id=contract.task_id,
        responsible_name=contract.responsible_name,
        responsible_email=contract.responsible_email,
        habit=contract.habit,
        description=contract.description,
        penalty=contract.penalty,
        start=contract.start.strftime("%Y-%m-%d"),
        end=contract.end.strftime("%Y-%m-%d"),
        status=0,
        supervisor_name=contract.supervisor_name,
        supervisor_email=contract.supervisor_email
    )
    
    last_record_id = await database.execute(query)
    return JSONResponse(status_code=201, content={"message": "Contract created successfully", "id": last_record_id})

@contract_route.put("/contract/{id}")
async def update_contract(id: str, contract_update: Contract):
    query_verify = contracts.select().where(contracts.c.id == id)
    if await database.fetch_one(query_verify) is None:
        return JSONResponse(status_code=404, content={"message": "Contract not found"})
    
    query_update = (contracts.update().where(contracts.c.id == id).values(contract_update.dict()))
    await database.execute(query_update)
    
    return JSONResponse(status_code=200, content={"message": "Contract updated successfully"})

@contract_route.put("/contract/{id}/activate")
async def activate_contract(id: str):
    query_verify = contracts.select().where(contracts.c.id == id)
    
    if await database.fetch_one(query_verify) is None:
        return JSONResponse(status_code=404, content={"message": "Contract not found"})
    
    query_update = contracts.update().where(contracts.c.id == id).values(status=1)
    await database.execute(query_update)
    
    return JSONResponse(status_code=200, content={"message": "Contract activated successfully"})

@contract_route.put("/contract/{id}/deactivate")
async def activate_contract(id: str):
    query_verify = contracts.select().where(contracts.c.id == id)
    
    if await database.fetch_one(query_verify) is None:
        return JSONResponse(status_code=404, content={"message": "Contract not found"})
    
    query_update = contracts.update().where(contracts.c.id == id).values(status=0)
    await database.execute(query_update)
    
    return JSONResponse(status_code=200, content={"message": "Contract activated successfully"})

@contract_route.post("/penalty")
async def create_penalty(contract: Contract):
    query_verify = contracts.select().where(contracts.c.id == contract.id)
    contract = await database.fetch_one(query_verify)
    
    if contract is None:
        return JSONResponse(status_code=404, content={"message": "Contract not found"})
    
    query_insert = penalties.insert().values(contract_id=contract.id, description=contract.penalty)
    await database.execute(query_insert)
    
    return JSONResponse(status_code=200, content={"message": "Contract penalty successfully"})

@contract_route.post("/streak")
async def create_streak(contract: Contract):
    query_verify = contracts.select().where(contracts.c.id == contract.id)
    contract = await database.fetch_one(query_verify)
    
    if contract is None:
        return JSONResponse(status_code=404, content={"message": "Contract not found"})
    
    query_insert = streaks.insert().values(contract_id=contract.id)
    await database.execute(query_insert)
    
    return JSONResponse(status_code=200, content={"message": "Contract streak successfully"})