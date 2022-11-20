from fastapi import HTTPException
from app.api.models import CreateDataSchema, TransferSchema
from app.db import account, customer, database


async def create_data(payload: CreateDataSchema):
    query = customer.insert().values(
        customer_number=payload.customer_number,
        name=payload.name
    )
    customer_id = await database.execute(query=query)

    query = account.insert().values(
        account_number=payload.account_number,
        customer_number=payload.customer_number,
        balance=payload.balance
    )
    await database.execute(query=query)
    
    return customer_id


async def get_all_account():
    query = account.select()
    return await database.fetch_all(query=query)


async def check_balance(account_number: int):
    query = account.select().where(account_number == account.c.account_number)
    acc = await database.fetch_one(query=query)
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")

    query = customer.select().where(acc['customer_number'] == customer.c.customer_number)
    cus = await database.fetch_one(query=query)
    if not cus:
        raise HTTPException(status_code=404, detail="Customer not found")

    response = {
        "account_number": acc['account_number'],
        "customer_name": cus['name'],
        "balance": acc['balance'],
    }
    return response


async def transfer(from_account_number: int, payload: TransferSchema):
    if int(payload.to_account_number) == from_account_number:
        raise HTTPException(status_code=404, detail="Cannot transfer into same account number")

    # from account
    query = account.select().where(from_account_number == account.c.account_number)
    from_acc = await database.fetch_one(query=query)
    if not from_acc:
        raise HTTPException(status_code=404, detail="From Account not found")

    # to account
    query = account.select().where(int(payload.to_account_number) == account.c.account_number)
    to_acc = await database.fetch_one(query=query)
    if not to_acc:
        raise HTTPException(status_code=404, detail="To Account not found")
    
    from_acc_balance = from_acc['balance'] - payload.amount

    if from_acc_balance < 0:
        raise HTTPException(status_code=404, detail="Balance not enough")

    to_acc_balance = to_acc['balance'] + payload.amount
    
    query = (
        account
        .update()
        .where(from_acc['id'] == account.c.id)
        .values(balance=from_acc_balance)
    )
    await database.execute(query=query)
    
    query = (
        account
        .update()
        .where(to_acc['id'] == account.c.id)
        .values(balance=to_acc_balance)
    )
    await database.execute(query=query)

    return True
