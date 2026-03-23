from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt

from auth.service import AuthService
from contactbook.service import ContactService
from database import get_db
from core.security import oauth2_scheme
from core.config import SECRET_KEY, ALGORITHM
from repository import users as repository_users


def get_contact_service(db: AsyncSession = Depends(get_db)):
    return ContactService(db)


def get_auth_service(db: AsyncSession = Depends(get_db)):
    return AuthService(db)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        token_type = payload.get("type")
        if token_type != "access_token":
            raise credentials_exception
        
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception

    user = await repository_users.get_user_by_email(email, db)
    if user is None:
        raise credentials_exception
        
    return user