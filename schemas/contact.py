from pydantic import BaseModel


class DataItem(BaseModel):
    phone: str 
    address: str


class PhoneResponse(BaseModel):
    phone: str
    address: str | None
