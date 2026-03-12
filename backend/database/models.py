from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

DATABASE_URL = "sqlite+aiosqlite:///./database/tickets.db"

engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False})
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, index=True)
    message = Column(String)
    status = Column(String, default="pending") # pending, resolved
    priority = Column(String, default="low")   # low, high
    category = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
