from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from src.schemas import auth as schemas
from src.utils import auth
from src.core.session import get_db
from src.utils import crud
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/register", response_model=schemas.Token)
async def register(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    created_user = await crud.create_user(db, user)
    token_data = {"sub": created_user.email, "role": created_user.user_role}
    token = auth.create_access_token(data=token_data)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=schemas.Token)
async def login(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):    
    db_user = await crud.get_user_by_email(db, user.email)
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not auth.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token_data = {"sub": db_user.email, "role": db_user.user_role}
    token = auth.create_access_token(data=token_data)
    return {"access_token": token, "token_type": "bearer"}
