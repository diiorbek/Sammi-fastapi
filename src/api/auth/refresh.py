from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession  
from src.core.base import get_db  
from src.utils.auth_util import create_access_token, verify_token, get_user  
from datetime import timedelta
from src.core.config import settings

router = APIRouter()

@router.post("/refresh")
async def refresh_token(
    request: Request, 
    db: AsyncSession = Depends(get_db)
):
    refresh_token_value = request.cookies.get("refresh_token")
    if not refresh_token_value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No refresh token provided"
        )

    payload = await verify_token(refresh_token_value, settings.REFRESH_SECRET_KEY)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    username = payload.get("sub")
    user = await get_user(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    new_access_token = await create_access_token(
        {"sub": user.username}, 
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {"access_token": new_access_token, "token_type": "bearer"}