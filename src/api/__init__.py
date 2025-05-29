from fastapi import APIRouter
from .auth import router as auth_router
from .videos import router as videos_router
from .course import router as course_router

main_router = APIRouter()
main_router.include_router(auth_router)
main_router.include_router(videos_router)
main_router.include_router(course_router)