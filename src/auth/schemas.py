from pydantic import BaseModel
from typing import Optional


class UserModel(BaseModel):
    username: str
    password: str


class TokenPayload(BaseModel):
    """
    JWT token payload structure.
    Used for validating the decoded token claims.
    """
    sub: str  # Subject - typically the user's email
    type: str  # Token type: 'access_token' or 'refresh_token'
    exp: int  # Expiration time (unix timestamp)


class TokenResponse(BaseModel):
    """
    Response model for token endpoints (login, refresh).
    """
    access_token: str
    token_type: str = "bearer"
    expires_in: Optional[int] = None  # Expiration time in seconds


class RefreshTokenRequest(BaseModel):
    """
    Request model for refresh token endpoint.
    """
    refresh_token: str