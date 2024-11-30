import uuid

from sqlmodel import Field, Relationship, SQLModel
from app.models.user import User

# Shared properties
class DeviceBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on Device creation
class DeviceCreate(DeviceBase):
    pass


# Properties to receive on Device update
class DeviceUpdate(DeviceBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Database model, database table inferred from class name
class Device(DeviceBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="devices")


# Properties to return via API, id is always required
class DevicePublic(DeviceBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class DevicesPublic(SQLModel):
    data: list[DevicePublic]
    count: int


# from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
# from sqlalchemy.orm import relationship
# from app.database.db import Base
# from datetime import datetime

# class Device(Base):
#     __tablename__ = 'devices'
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     type = Column(String)
#     status = Column(String)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
#     tasks = relationship("Task", back_populates="device")