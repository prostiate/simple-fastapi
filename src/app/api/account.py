from typing import List
from fastapi import APIRouter, Path
from app.api import crud
from app.api.models import GetAllAccountSchema, CreateDataDB, CreateDataSchema, CheckBalanceSchema, TransferSchema

router = APIRouter()


@router.get("/", response_model=List[GetAllAccountSchema])
async def get_all_accounts():
    return await crud.get_all_account()


@router.post("/create_data", response_model=CreateDataDB, status_code=201)
async def create_data(payload: CreateDataSchema):
    customer_id = await crud.create_data(payload=payload)

    response_object = {
        "id": customer_id,
        "account_number": payload.account_number,
        "customer_number": payload.customer_number,
        "name": payload.name,
        "balance": payload.balance,
    }
    return response_object


@router.get("/{account_number}/", response_model=CheckBalanceSchema)
async def check_balance(account_number: int = Path(..., gt=0)):
    return await crud.check_balance(account_number=account_number)


@router.post("/{from_account_number}/transfer", status_code=201)
async def transfer(payload: TransferSchema, from_account_number: int = Path(..., gt=0)):
    await crud.transfer(from_account_number=from_account_number, payload=payload)
    return payload
