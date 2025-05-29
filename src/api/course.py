from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from src.core.session import get_db
from src.model.course import Course
from src.schemas.course import CourseCreate, CourseUpdate, CourseOut

router = APIRouter(
    prefix="/courses",
    tags=["courses"]
)

@router.post("/", response_model=CourseOut)
async def create_new_course(course: CourseCreate, db: AsyncSession = Depends(get_db)):
    db_course = Course(**course.model_dump())
    db.add(db_course)
    await db.commit() 
    await db.refresh(db_course) 
    return db_course

@router.get("/", response_model=list[CourseOut])
async def read_courses(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).offset(skip).limit(limit))  
    courses = result.scalars().all()  
    return courses

@router.get("/{course_id}", response_model=CourseOut)
async def read_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).filter(Course.id == course_id)) 
    course = result.scalars().first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.put("/{course_id}", response_model=CourseOut)
async def update_existing_course(course_id: int, course: CourseUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).filter(Course.id == course_id))  
    db_course = result.scalars().first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    for key, value in course.model_dump().items():
        setattr(db_course, key, value)

    await db.commit()
    await db.refresh(db_course)
    return db_course

@router.delete("/{course_id}")
async def delete_existing_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).filter(Course.id == course_id))  
    db_course = result.scalars().first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")

    await db.delete(db_course)  
    await db.commit() 
    return {"message": "Course deleted"}
