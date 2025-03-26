from sqlalchemy import Column , String , Integer , Float , ForeignKey , Enum
from sqlalchemy.dialects.postgresql import JSONB
from src.core.base import Base
from enum import Enum

class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    DELIVERED = "delivered"
    CANCELED = "canceled"


class Booking(Base):
    __tablename__ = "bookings"


    id = Column(Integer , primary_key=True , nullable=False)
    user_id = Column(Integer , ForeignKey("users.id"))
    courier_id = Column(Integer , ForeignKey("users.id") , nullable=True)
    store_id = Column(Integer, ForeignKey("stories.id"))
    total_price = Column(Float , nullable=False)
    location = Column(String , nullable=False)

    order_details = Column(JSONB , nullable=False)
    status = Column(Enum(OrderStatus) , nullable=False , default=OrderStatus.PENDING)

