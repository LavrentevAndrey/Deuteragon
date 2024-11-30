from fastapi import APIRouter
from app.api.routers import device_router, task_router, telemetry_router, user_router

api_router = APIRouter()

api_router.include_router(device_router, prefix="/api")
api_router.include_router(task_router, prefix="/api")
api_router.include_router(telemetry_router, prefix="/api")
api_router.include_router(user_router, prefix="/api")