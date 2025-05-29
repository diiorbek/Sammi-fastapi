from sqlalchemy.orm import Session
from src.model.user import User
from src.schemas import auth as schemas
from . import auth
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    return user

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    hashed_password = auth.hash_password(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        user_role=user.user_role
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
