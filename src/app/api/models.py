from pydantic import BaseModel, Field


class CreateDataSchema(BaseModel):
    account_number: int = Field(..., gt=0)
    customer_number: int = Field(..., gt=0)
    balance: int = Field(..., gt=0) 
    name: str = Field(..., min_length=3, max_length=50)


class GetAllAccountSchema(BaseModel):
    account_number: int
    customer_number: int
    balance: int 
    id: int 


class CreateDataDB(CreateDataSchema):
    id: int


class CheckBalanceSchema(BaseModel):
    account_number: str
    customer_name: str
    balance: int


class TransferSchema(BaseModel):
    to_account_number: str
    amount: int


class GetAllCustomerSchema(BaseModel):
    id: int
    customer_number: int = Field(..., title="heheh")
    name: str = Field(..., min_length=3, max_length=50)
