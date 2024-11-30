from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db import get_db
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate, User
from typing import List

router = APIRouter()

@router.post("/users", response_model=User)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@router.get("/users", response_model=List[User])
async def read_users(db: AsyncSession = Depends(get_db)):
    users = await db.execute(User.__table__.select())
    return users.scalars().all()

@router.get("/users/{id}", response_model=User)
async def read_user(id: int, db: AsyncSession = Depends(get_db)):
    user = await db.execute(User.__table__.select().where(User.id == id))
    user = user.scalar()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{id}", response_model=User)
async def update_user(id: int, user: UserUpdate, db: AsyncSession = Depends(get_db)):
    db_user = await db.execute(User.__table__.select().where(User.id == id))
    db_user = db_user.scalar()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.dict().items():
        setattr(db_user, key, value)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@router.delete("/users/{id}", response_model=User)
async def delete_user(id: int, db: AsyncSession = Depends(get_db)):
    user = await db.execute(User.__table__.select().where(User.id == id))
    user = user.scalar()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(user)
    await db.commit()
    return user