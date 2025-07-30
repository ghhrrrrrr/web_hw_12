from typing import List
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from contactbook.service import ContactService
from database import Base, get_db
from contactbook.models import Contact
from contactbook.schemas import ContactSchema, ContactCreate, ContactFind, ContactUpdate
from dependencies import get_contact_service



router = APIRouter()
    
    
@router.get('', response_model=List[ContactSchema])
async def get_contacts(contact: ContactFind = Depends(), service: ContactService = Depends(get_contact_service)):
    return await service.get_contact(contact)
    
        
@router.post('', response_model=ContactSchema)
async def create_contact(contact: ContactCreate, service: ContactService = Depends(get_contact_service)):
    return await service.create_contact(contact)
    
    

@router.patch('/{id}', response_model=ContactSchema)
async def update_contact(id: int, contact: ContactUpdate, service: ContactService = Depends(get_contact_service)):
    return await service.update_contact(id, contact)
    
    
@router.delete('/{id}')
async def delete_contact(id: int, service: ContactService = Depends(get_contact_service)):
    return await service.delete_contact(id)

@router.get('/birthdays')
async def get_upcoming_birthdays(service: ContactService = Depends(get_contact_service)):
    return await service.get_upcoming_birthdays()