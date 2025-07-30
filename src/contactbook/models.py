from sqlalchemy import Date
from datetime import date
from sqlalchemy.orm import Mapped, mapped_column
from database import Base



class Contact(Base):
    __tablename__ = 'contacts'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] 
    surname: Mapped[str] 
    email: Mapped[str]
    phone: Mapped[str]
    birthdate: Mapped[date] = mapped_column(Date)
    
    