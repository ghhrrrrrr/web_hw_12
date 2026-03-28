from typing import TYPE_CHECKING
from sqlalchemy import Date, ForeignKey
from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

if TYPE_CHECKING:
    from models.user import User



class Contact(Base):
    __tablename__ = 'contacts'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] 
    surname: Mapped[str] 
    email: Mapped[str]
    phone: Mapped[str]
    birthdate: Mapped[date] = mapped_column(Date)
    
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    owner: Mapped['User'] = relationship(back_populates='contacts')
    
    