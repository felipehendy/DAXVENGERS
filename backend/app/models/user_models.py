from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    xp: int = 0
    coins: int = 0
    level: int = 1
    streak_days: int = 0
    is_premium: bool = False
    created_at: Optional[datetime] = None

class UserUpdate(BaseModel):
    username: Optional[str] = None
    xp: Optional[int] = None
    coins: Optional[int] = None
    level: Optional[int] = None
    streak_days: Optional[int] = None
    is_premium: Optional[bool] = None

class LoginRequest(BaseModel):
    email: str
    password: str