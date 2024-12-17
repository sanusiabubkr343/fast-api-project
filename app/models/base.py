from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = "sqlite://db.sqlite3"

# Async engine for SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)

# Session maker for handling database sessions
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Base class for models
Base = declarative_base()
