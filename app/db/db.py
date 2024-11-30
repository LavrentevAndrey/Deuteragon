from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config.db_config import DATABASE_URL

# Create the SQLAlchemy async engine
engine = create_async_engine(DATABASE_URL, future=True, echo=True)

# Create a SessionLocal class for session management
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Base class for declarative models
Base = declarative_base()

# Dependency to get an asynchronous database session
async def get_db():
    async with AsyncSessionLocal() as db:
        yield db
        await db.commit()