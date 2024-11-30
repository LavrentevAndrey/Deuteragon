from .device_router import router as device_router
from .task_router import router as task_router
from .telemetry_router import router as telemetry_router
from .user_router import router as user_router

__all__ = [
    "device_router",
    "task_router",
    "telemetry_router",
    "user_router",
]