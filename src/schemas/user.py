from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime
from typing import Optional

class UserRole(str, Enum):
    user = "user"
    admin = "admin"

class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool = True
    role: UserRole

class UserCreate(UserBase):
    password: str

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: UserRole

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[UserRole] = None

class UserOut(UserBase):
    id: int
    data_joined: datetime
    
    class Config:
        from_attributes = True
