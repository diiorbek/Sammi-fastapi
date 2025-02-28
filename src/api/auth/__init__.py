from fastapi import APIRouter
from .login import router as login
from .signup import router as signup
from .logout import router as logout
from .refresh import router as refresh


auth_router = APIRouter(
    tags=["Auth"],
    prefix="/auth"
)


auth_router.include_router(login)
auth_router.include_router(signup)
auth_router.include_router(logout)
auth_router.include_router(refresh)
