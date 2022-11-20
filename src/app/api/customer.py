from typing import List
from fastapi import APIRouter
from app.api.models import GetAllCustomerSchema
from app.db import customer, database

router = APIRouter()


@router.get("/", response_model=List[GetAllCustomerSchema])
async def get_all_customers():
    query = customer.select()
    return await database.fetch_all(query=query)
