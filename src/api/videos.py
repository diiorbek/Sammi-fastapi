from fastapi import APIRouter, UploadFile, File, Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
import os
from src.model.course import Course  
from src.core.session import get_db
from src.model.video import Video
from src.schemas.video import VideoCreate, VideoRead
from fastapi import Form

router = APIRouter(
    prefix="/videos",
    tags=["videos"],
)   

@router.post("/", response_model=VideoRead)
async def upload_video(
    request: Request,
    title: str = Form(...),
    course_id: int = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail=f"Course with id {course_id} not found")

    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    file_url = f"{request.base_url}uploads/{file.filename}"

    new_video = Video(
        title=title,
        course_id=course_id,
        file_url=file_url
    )
    db.add(new_video)
    await db.commit()
    await db.refresh(new_video)

    return new_video


@router.get("/", response_model=List[VideoRead])
async def get_all_videos(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Video))
    videos = result.scalars().all()
    return videos


@router.get("/{video_id}", response_model=VideoRead)
async def get_video(video_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Video).where(Video.id == video_id))
    video = result.scalar_one_or_none()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video


@router.put("/{video_id}", response_model=VideoRead)
async def update_video(
    video_id: int,
    request: Request,
    title: Optional[str] = Form(None),
    course_id: Optional[int] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Video).where(Video.id == video_id))
    video = result.scalar_one_or_none()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    if title is not None:
        video.title = title
    if course_id is not None:
        video.course_id = course_id

    if file is not None:
        os.makedirs("uploads", exist_ok=True)
        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(await file.read())
        video.file_url = f"{request.base_url}uploads/{file.filename}"

    db.add(video)
    await db.commit()
    await db.refresh(video)
    return video


@router.delete("/{video_id}")
async def delete_video(video_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Video).where(Video.id == video_id))
    video = result.scalar_one_or_none()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    await db.delete(video)
    await db.commit()
    return {"message": f"Video with id {video_id} deleted successfully"}

