from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db import get_db
from app.models.task_model import Task
from app.schemas.task_schema import TaskCreate, TaskUpdate, Task
from app.models.device_model import Device
from typing import List

router = APIRouter()

@router.post("/tasks", response_model=Task)
async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    db_device = await db.execute(Device.__table__.select().where(Device.id == task.device_id))
    db_device = db_device.scalar()
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    db_task = Task(**task.dict())
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task

@router.get("/tasks", response_model=List[Task])
async def read_tasks(db: AsyncSession = Depends(get_db)):
    tasks = await db.execute(Task.__table__.select())
    return tasks.scalars().all()

@router.get("/tasks/{id}", response_model=Task)
async def read_task(id: int, db: AsyncSession = Depends(get_db)):
    task = await db.execute(Task.__table__.select().where(Task.id == id))
    task = task.scalar()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{id}", response_model=Task)
async def update_task(id: int, task: TaskUpdate, db: AsyncSession = Depends(get_db)):
    db_task = await db.execute(Task.__table__.select().where(Task.id == id))
    db_task = db_task.scalar()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task.dict().items():
        setattr(db_task, key, value)
    await db.commit()
    await db.refresh(db_task)
    return db_task

@router.delete("/tasks/{id}", response_model=Task)
async def delete_task(id: int, db: AsyncSession = Depends(get_db)):
    task = await db.execute(Task.__table__.select().where(Task.id == id))
    task = task.scalar()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    await db.delete(task)
    await db.commit()
    return task