from fastapi import FastAPI
from app.routers import device_router, task_router, telemetry_router, user_router

app = FastAPI()

app.include_router(device_router, prefix="/api")
app.include_router(task_router, prefix="/api")
app.include_router(telemetry_router, prefix="/api")
app.include_router(user_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Deuteragon: Management and Monitoring System!"}