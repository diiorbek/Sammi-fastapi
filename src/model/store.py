from sqlalchemy import Column , Integer , String, Float 
from sqlalchemy.dialects.postgresql import JSONB
from model.base import Base


class Store(Base):
    __tablename__ = "stories"

    id = Column(Integer , primary_key=True , index=True)
    name = Column(String , nullable=False)
    description = Column(String , nullable=False)
    liter_price = Column(JSONB , nullable=False)
    delivery_price = Column(Float , nullable=False , default=0)
