from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession 
from datetime import timedelta
from core.session import get_db  
from utils.auth_util import (
    authenticate_user,
    create_access_token, 
    create_refresh_token,
)
from src.core.config import app_settings

router = APIRouter()

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):

    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username and password"
        )

    if user.is_active is True:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already logged in"
        )
    

    user.is_active = True
    await db.commit()        
    await db.refresh(user)   


    access_token = await create_access_token(
        {"sub": user.username},
        timedelta(minutes=app_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = await create_refresh_token(
        {"sub": user.username},
        timedelta(days=app_settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
 