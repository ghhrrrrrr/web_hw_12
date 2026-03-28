from datetime import date, timedelta
from fastapi import HTTPException, status
from sqlalchemy import extract, select
from sqlalchemy.ext.asyncio import AsyncSession

from contactbook.models import Contact
from contactbook.schemas import ContactCreate, ContactFind, ContactUpdate
from models.user import User



class ContactService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_contact(self, contact: ContactFind, user: User):
        stmt = select(Contact)
    
        if contact.id:
            stmt = stmt.where(Contact.id == contact.id)
        if contact.email:
            stmt = stmt.where(Contact.email == contact.email)
        if contact.name:
            stmt = stmt.where(Contact.name == contact.name) 
        if contact.surname:
            stmt = stmt.where(Contact.surname == contact.surname)
        
        stmt = stmt.where(Contact.user_id == user.id)
    
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def create_contact(self, contact: ContactCreate, user: User):
        contact_json = contact.model_dump()
        contact_json['user_id'] = user.id
        db_contact = Contact(**contact_json)
        self.db.add(db_contact)
        await self.db.commit()
        await self.db.refresh(db_contact)
        return db_contact
    
    async def update_contact(self, id: int, contact: ContactUpdate, user: User):
        stmt = select(Contact).where(Contact.id == id)
        result = await self.db.execute(stmt)
        db_contact = result.scalar_one_or_none()
        if db_contact is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
        if db_contact.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
        
        contact_json = contact.model_dump(exclude_none=True)
        for key, value in contact_json.items():
            setattr(db_contact, key, value)
        await self.db.commit()
        await self.db.refresh(db_contact)
        return db_contact
    
    async def delete_contact(self, id: int, user: User):
        stmt = select(Contact).where(Contact.id == id)
        result = await self.db.execute(stmt)
        db_contact = result.scalar_one_or_none()
        if db_contact.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
        if db_contact:
            await self.db.delete(db_contact)
            await self.db.commit()    
        return {"message": "Contact deleted successfully"}
    
    async def get_upcoming_birthdays(self, user: User):
        today = date.today()
        limit = today + timedelta(days=7)
        
        stmt = select(Contact).where(
            ((extract('month', Contact.birthdate) == today.month) & 
                (extract('day', Contact.birthdate) >= today.day)) |
            ((extract('month', Contact.birthdate) == limit.month) & 
                (extract('day', Contact.birthdate) <= limit.day)) &
            (Contact.user_id == user.id)
        )
        
        result = await self.db.execute(stmt)
        return result.scalars().all()