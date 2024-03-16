from fastapi import APIRouter
from .jwt_auth.router import router as jwt_auth_router

router = APIRouter()

router.include_router(jwt_auth_router, prefix="/auth", tags=["auth"])
