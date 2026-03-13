import os
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.future import select
from datetime import datetime, UTC

DATABASE_PATH = os.getenv("DATABASE_PATH", "./database/tickets.db")
DATABASE_URL = f"sqlite+aiosqlite:///{DATABASE_PATH}"

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
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))

async def init_db():
    db_exists = os.path.exists(DATABASE_PATH)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    if not db_exists:
        print("Database not found. Creating and seeding initial data...")
        from services.ai.gemini import ai_service
        
        tickets_to_seed = [
            {"customer_name": "Alice Smith", "message": "I can't log in to my account. It says 'invalid credentials' even after a password reset."},
            {"customer_name": "Bob Johnson", "message": "I'd like to request a refund for my last invoice #12345. I was double charged."},
            {"customer_name": "Charlie Brown", "message": "The dashboard is loading very slowly today. It takes about 30 seconds to see my stats."},
            {"customer_name": "Diana Prince", "message": "Is there a way to export my data to a CSV format? I couldn't find it in the settings."},
            {"customer_name": "Edward Norton", "message": "Your service is down again! This is the third time this week. I'm losing money!"},
            {"customer_name": "Fiona Gallagher", "message": "I want to upgrade my plan to the Enterprise tier. Who should I talk to?"},
            {"customer_name": "George Miller", "message": "Can you add support for dark mode? My eyes are hurting at night."},
            {"customer_name": "Hannah Abbott", "message": "I found a typo on the landing page, 'Suport' should be 'Support'."},
            {"customer_name": "Ian McKellen", "message": "My payment failed but my credit card was still charged. Please check ASAP."},
            {"customer_name": "Julia Roberts", "message": "Just wanted to say that your new UI looks amazing! Great job team."}
        ]
        
        async with AsyncSessionLocal() as session:
            for ticket_data in tickets_to_seed:
                ai_result = await ai_service.classify_ticket(ticket_data["message"])
                new_ticket = Ticket(
                    customer_name=ticket_data["customer_name"],
                    message=ticket_data["message"],
                    category=ai_result.get("category", "General Support"),
                    priority=ai_result.get("priority", "low")
                )
                session.add(new_ticket)
            await session.commit()
        print("Database seeded successfully with 10 records.")
    else:
        print("Database already exists. Skipping seeding.")
