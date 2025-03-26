from sqlalchemy import Column , Integer , String, DateTime, Enum, Boolean
from sqlalchemy.sql import func
from src.core.base import Base
import enum

class UserRole(enum.Enum):
    user = "user"
    admin = "admin"
    courier = "courier"
    owner = "owner"

    

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer , primary_key=True , nullable=False)
    username = Column(String(100), nullable=False)
    password = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String , nullable=True)
    is_active = Column(Boolean , default=False)
    role = Column(Enum(UserRole) , default=UserRole.user)
    data_joined = Column(DateTime , default=func.now())