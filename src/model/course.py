from sqlalchemy import Column, Integer, String
from .base import Base
from sqlalchemy.orm import relationship


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True, nullable=False)
    image_url = Column(String, nullable=False)
    description = Column(String, nullable=False) 
