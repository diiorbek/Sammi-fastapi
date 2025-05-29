from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Literal

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    user_role: Literal["user", "admin"]

class UserOut(BaseModel):
    id: int
    email: EmailStr
    joined_date: datetime
    user_role: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
