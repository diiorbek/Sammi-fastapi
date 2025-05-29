from pydantic import BaseModel, HttpUrl
from typing import Optional


class VideoBase(BaseModel):
    id: int
    title: str
    course_id: int


class VideoCreate(VideoBase):
    pass


class VideoRead(VideoBase):
    file_url: HttpUrl

    class Config:
        from_attributes = True
