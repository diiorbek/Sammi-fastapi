from fastapi import APIRouter , Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.base import get_db
from src.schemas.booking import BookingCreate
from src.model.booking import Booking

booking_router = APIRouter()


@booking_router.post("/create")
async def create_book(
    booking_item: BookingCreate,  
    db :AsyncSession = Depends(get_db)
    ):
    new_booking = Booking(**booking_item.model_dump())
    

    pass
