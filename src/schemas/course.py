from pydantic import BaseModel

class CourseBase(BaseModel):
    title: str
    image_url: str
    description: str

class CourseCreate(CourseBase):
    pass

class CourseUpdate(CourseBase):
    pass

class CourseOut(CourseBase):
    id: int

    class Config:
        from_attributes = True
