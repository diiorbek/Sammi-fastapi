from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select  
from schemas.user import RegisterRequest
from core.session import get_db  
from model.user import User
from utils.auth_util import hash_password

router = APIRouter()

@router.post("/signup")
async def register(user_data: RegisterRequest, db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(User).filter(User.username == user_data.username))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    
    new_user = User(
        username=user_data.username,
        password=await hash_password(user_data.password),
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        is_active=False,  
        role=user_data.role.value
)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)


    return  new_user