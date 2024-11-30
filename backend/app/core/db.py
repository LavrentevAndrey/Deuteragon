from sqlmodel import Session, create_engine, select

from app import crud
from app.core.config import settings
from app.models.user import User, UserCreate

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def init_db(session: Session) -> None:
    from sqlmodel import SQLModel

    SQLModel.metadata.create_all(engine)

    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.create_user(session=session, user_create=user_in)

# TODO: Add asynchronious CRUD like this?
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# from config.db_config import DATABASE_URL

# # Create the SQLAlchemy async engine
# engine = create_async_engine(DATABASE_URL, future=True, echo=True)

# # Create a SessionLocal class for session management
# AsyncSessionLocal = sessionmaker(
#     bind=engine,
#     class_=AsyncSession,
#     expire_on_commit=False,
# )

# # Base class for declarative models
# Base = declarative_base()

# # Dependency to get an asynchronous database session
# async def init_db():
#     async with AsyncSessionLocal() as db:
#         yield db
#         await db.commit()