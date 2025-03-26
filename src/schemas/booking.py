from pydantic import BaseModel
from typing import Dict , Any , Optional
from enum import Enum

class OrderStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    delivered = "delivered"
    canceled = "canceled"

class BookingBase(BaseModel):
    store_id: int 
    total_price: float 
    location: str 
    order_details: Dict[str, Any] 

class BookingCreate(BookingBase):
    pass


class BookingUpdate(BaseModel):
    store_id: Optional[int] 
    total_price: Optional[float]
    location: Optional[str]
    order_details: Optional[Dict[str, Any]] 



class BookingResponse(BookingBase):
    id: int
    user_id: int
    courier_id: Optional[int] 
    status: OrderStatus 
