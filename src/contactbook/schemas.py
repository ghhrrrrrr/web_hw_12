from pydantic import BaseModel, ConfigDict
from datetime import date

class ContactCreate(BaseModel):
    name: str 
    surname: str 
    email: str
    phone: str
    birthdate: date

class ContactSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str 
    surname: str 
    email: str
    phone: str
    birthdate: date

class ContactFind(BaseModel):
    id: int | None = None
    name: str | None = None
    surname: str | None = None
    email: str | None = None
    
class ContactUpdate(BaseModel):
    name: str | None = None
    surname: str | None = None
    email: str | None = None
    phone: str | None = None
    birthdate: date | None = None
