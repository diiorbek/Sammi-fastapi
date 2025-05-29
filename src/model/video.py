from sqlalchemy import Column, Integer, String, ForeignKey
from .base import Base

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    file_url = Column(String, nullable=False)
