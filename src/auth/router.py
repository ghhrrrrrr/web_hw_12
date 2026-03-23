from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from dependencies import get_auth_service
from models.user import User
from auth.schemas import UserModel, RefreshTokenRequest
from auth.service import AuthService

router = APIRouter()


@router.post("/signup")
async def signup(body: UserModel, service: AuthService = Depends(get_auth_service)):
    return await service.signup(body)


@router.post("/login")
async def login(body: OAuth2PasswordRequestForm = Depends(), service: AuthService = Depends(get_auth_service)):
    return await service.login(body)


@router.post("/refresh_token")
async def refresh_token(body: RefreshTokenRequest, service: AuthService = Depends(get_auth_service)):
    return await service.refresh_token(body)

