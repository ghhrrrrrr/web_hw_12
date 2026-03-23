from typing import List
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from contactbook.service import ContactService
from database import Base, get_db
from dependencies import get_contact_service, get_current_user
from contactbook.models import Contact
from contactbook.schemas import ContactSchema, ContactCreate, ContactFind, ContactUpdate
from models.user import User



router = APIRouter()
    
    
@router.get('', response_model=List[ContactSchema])
async def get_contacts(contact: ContactFind = Depends(), service: ContactService = Depends(get_contact_service), current_user: User = Depends(get_current_user)):
    return await service.get_contact(contact)
    
        
@router.post('', response_model=ContactSchema)
async def create_contact(contact: ContactCreate, service: ContactService = Depends(get_contact_service), current_user: User = Depends(get_current_user)):
    return await service.create_contact(contact)
    

@router.patch('/{contact_id}', response_model=ContactSchema)
async def update_contact(contact_id: int, contact: ContactUpdate, service: ContactService = Depends(get_contact_service), current_user: User = Depends(get_current_user)):
    return await service.update_contact(contact_id, contact)
    
    
@router.delete('/{contact_id}')
async def delete_contact(contact_id: int, service: ContactService = Depends(get_contact_service), current_user: User = Depends(get_current_user)):
    return await service.delete_contact(contact_id)

@router.get('/birthdays')
async def get_upcoming_birthdays(service: ContactService = Depends(get_contact_service), current_user: User = Depends(get_current_user)):
    return await service.get_upcoming_birthdays()