from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from auth.schemas import UserModel, RefreshTokenRequest
from core.security import get_password_hash, verify_password, create_access_token, create_refresh_token, decode_refresh_token


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def signup(self, body: UserModel):
        stmt = select(User).where(User.email == body.username)
        result = await self.db.execute(stmt)
        exist_user = result.scalar_one_or_none()
        if exist_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
        new_user = User(email=body.username, password=get_password_hash(body.password))
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return {"new_user": new_user.email}
    
    
    async def login(self, body: OAuth2PasswordRequestForm ):
        stmt = select(User).where(User.email == body.username)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
        if not verify_password(body.password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")

        access_token = await create_access_token(data={"sub": user.email})
        refresh_token = await create_refresh_token(data={"sub": user.email})
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    
    async def refresh_token(self, body: RefreshTokenRequest):
        email = await decode_refresh_token(body.refresh_token)
        
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        
        access_token = await create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}
        
    