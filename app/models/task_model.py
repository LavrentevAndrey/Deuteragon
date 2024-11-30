from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.db import Base
from datetime import datetime

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    scheduled_at = Column(DateTime)
    device_id = Column(Integer, ForeignKey("devices.id"))
    device = relationship("Device", back_populates="tasks")