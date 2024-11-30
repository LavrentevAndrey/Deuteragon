from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class DeviceBase(BaseModel):
    name: str
    type: str
    status: str

class DeviceCreate(DeviceBase):
    pass

class DeviceUpdate(DeviceBase):
    pass

class Device(DeviceBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    tasks: List[Optional["Task"]] = []

    class Config:
        orm_mode = True