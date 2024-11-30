from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db import get_db
from app.models.device_model import Device
from app.schemas.device_schema import DeviceCreate, DeviceUpdate, Device
from typing import List

router = APIRouter()

@router.post("/devices", response_model=Device)
async def create_device(device: DeviceCreate, db: AsyncSession = Depends(get_db)):
    db_device = Device(**device.dict())
    db.add(db_device)
    await db.commit()
    await db.refresh(db_device)
    return db_device

@router.get("/devices", response_model=List[Device])
async def read_devices(db: AsyncSession = Depends(get_db)):
    devices = await db.execute(Device.__table__.select())
    return devices.scalars().all()

@router.get("/devices/{id}", response_model=Device)
async def read_device(id: int, db: AsyncSession = Depends(get_db)):
    device = await db.execute(Device.__table__.select().where(Device.id == id))
    device = device.scalar()
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

@router.put("/devices/{id}", response_model=Device)
async def update_device(id: int, device: DeviceUpdate, db: AsyncSession = Depends(get_db)):
    db_device = await db.execute(Device.__table__.select().where(Device.id == id))
    db_device = db_device.scalar()
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    for key, value in device.dict().items():
        setattr(db_device, key, value)
    await db.commit()
    await db.refresh(db_device)
    return db_device

@router.delete("/devices/{id}", response_model=Device)
async def delete_device(id: int, db: AsyncSession = Depends(get_db)):
    device = await db.execute(Device.__table__.select().where(Device.id == id))
    device = device.scalar()
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    await db.delete(device)
    await db.commit()
    return device