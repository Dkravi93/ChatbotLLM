import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# ✅ Async engine for FastAPI
async_engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# ✅ Sync engine for Alembic (replace asyncpg → psycopg2)
SYNC_DATABASE_URL = DATABASE_URL.replace("asyncpg", "psycopg2")
sync_engine = create_engine(SYNC_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

# ✅ Base class for models
Base = declarative_base()

# Dependency for FastAPI (async session)
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
