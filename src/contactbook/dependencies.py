from fastapi import Depends
from contactbook.service import ContactService
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

def get_contact_service(db: AsyncSession = Depends(get_db)):
    return ContactService(db)