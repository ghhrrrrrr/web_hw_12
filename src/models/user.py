from typing import TYPE_CHECKING, List
from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from contactbook.models import Contact

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] 
    password_hash: Mapped[str] = mapped_column(String(255))
    
    contacts: Mapped[List["Contact"]] = relationship(back_populates="owner")