import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.status import CurrentUser, SessionDep
from app.models.device import Device, DeviceCreate, DevicePublic, DevicesPublic, DeviceUpdate
from app.models.service import Message

router = APIRouter()


@router.get("/", response_model=DevicesPublic)
def read_devices(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve devices.
    """

    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Device)
        count = session.exec(count_statement).one()
        statement = select(Device).offset(skip).limit(limit)
        devices = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Device)
            .where(Device.owner_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Device)
            .where(Device.owner_id == current_user.id)
            .offset(skip)
            .limit(limit)
        )
        devices = session.exec(statement).all()

    return DevicesPublic(data=devices, count=count)


@router.get("/{id}", response_model=DevicePublic)
def read_device(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get device by ID.
    """
    device = session.get(Device, id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    if not current_user.is_superuser and (device.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return device


@router.post("/", response_model=DevicePublic)
def create_device(
    *, session: SessionDep, current_user: CurrentUser, device_in: DeviceCreate
) -> Any:
    """
    Create new device.
    """
    device = Device.model_validate(device_in, update={"owner_id": current_user.id})
    session.add(device)
    session.commit()
    session.refresh(device)
    return device


@router.put("/{id}", response_model=DevicePublic)
def update_device(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    device_in: DeviceUpdate,
) -> Any:
    """
    Update an device.
    """
    device = session.get(Device, id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    if not current_user.is_superuser and (device.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    update_dict = device_in.model_dump(exclude_unset=True)
    device.sqlmodel_update(update_dict)
    session.add(device)
    session.commit()
    session.refresh(device)
    return device


@router.delete("/{id}")
def delete_device(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete an device.
    """
    device = session.get(Device, id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    if not current_user.is_superuser and (device.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    session.delete(device)
    session.commit()
    return Message(message="Device deleted successfully")


# TODO: Implement Async
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession
# from app.database.db import get_db
# from app.models.device_model import Device
# from app.schemas.device_schema import DeviceCreate, DeviceUpdate, Device
# from typing import List

# router = APIRouter()

# @router.post("/devices", response_model=Device)
# async def create_device(device: DeviceCreate, db: AsyncSession = Depends(get_db)):
#     db_device = Device(**device.dict())
#     db.add(db_device)
#     await db.commit()
#     await db.refresh(db_device)
#     return db_device

# @router.get("/devices", response_model=List[Device])
# async def read_devices(db: AsyncSession = Depends(get_db)):
#     devices = await db.execute(Device.__table__.select())
#     return devices.scalars().all()

# @router.get("/devices/{id}", response_model=Device)
# async def read_device(id: int, db: AsyncSession = Depends(get_db)):
#     device = await db.execute(Device.__table__.select().where(Device.id == id))
#     device = device.scalar()
#     if device is None:
#         raise HTTPException(status_code=404, detail="Device not found")
#     return device

# @router.put("/devices/{id}", response_model=Device)
# async def update_device(id: int, device: DeviceUpdate, db: AsyncSession = Depends(get_db)):
#     db_device = await db.execute(Device.__table__.select().where(Device.id == id))
#     db_device = db_device.scalar()
#     if db_device is None:
#         raise HTTPException(status_code=404, detail="Device not found")
#     for key, value in device.dict().items():
#         setattr(db_device, key, value)
#     await db.commit()
#     await db.refresh(db_device)
#     return db_device

# @router.delete("/devices/{id}", response_model=Device)
# async def delete_device(id: int, db: AsyncSession = Depends(get_db)):
#     device = await db.execute(Device.__table__.select().where(Device.id == id))
#     device = device.scalar()
#     if device is None:
#         raise HTTPException(status_code=404, detail="Device not found")
#     await db.delete(device)
#     await db.commit()
#     return device