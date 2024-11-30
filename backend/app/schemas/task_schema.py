from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TaskBase(BaseModel):
    description: str
    status: str
    scheduled_at: datetime
    device_id: int

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True