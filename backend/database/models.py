import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.future import select
from datetime import datetime, UTC

# Load .env.development from project root for local dev
# backend/database/models.py -> parents[2] = repo root
_ROOT_ENV = Path(__file__).resolve().parents[2] / ".env.development"
load_dotenv(dotenv_path=_ROOT_ENV, override=False)
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env.development", override=False)
load_dotenv(override=False)

DATABASE_PATH = os.getenv("DATABASE_PATH", "./database/tickets.db")
DATABASE_URL = f"sqlite+aiosqlite:///{DATABASE_PATH}"

# Ensure parent directory exists immediately at import time (handles docker volume and local dev)
Path(DATABASE_PATH).parent.mkdir(parents=True, exist_ok=True)

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
    db_path = Path(DATABASE_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Robust seeding: check row count, not just file existence
    # Covers case where file exists but is empty (e.g., failed previous seed, volume mount)
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Ticket))
        existing_tickets = result.scalars().all()
        if existing_tickets:
            print(f"Database already exists with {len(existing_tickets)} records. Skipping seeding.")
            return

    print("Database not found or empty. Creating and seeding initial data...")

    from services.ai.spark import ai_service

    # Deterministic fallback categories/priorities for prototype - used if AI unavailable
    tickets_to_seed = [
        {"customer_name": "Alice Smith", "message": "I can't log in to my account. It says 'invalid credentials' even after a password reset.", "fallback_category": "Technical Support", "fallback_priority": "high"},
        {"customer_name": "Bob Johnson", "message": "I'd like to request a refund for my last invoice #12345. I was double charged.", "fallback_category": "Billing", "fallback_priority": "high"},
        {"customer_name": "Charlie Brown", "message": "The dashboard is loading very slowly today. It takes about 30 seconds to see my stats.", "fallback_category": "Technical Support", "fallback_priority": "low"},
        {"customer_name": "Diana Prince", "message": "Is there a way to export my data to a CSV format? I couldn't find it in the settings.", "fallback_category": "Feature Request", "fallback_priority": "low"},
        {"customer_name": "Edward Norton", "message": "Your service is down again! This is the third time this week. I'm losing money!", "fallback_category": "Technical Support", "fallback_priority": "high"},
        {"customer_name": "Fiona Gallagher", "message": "I want to upgrade my plan to the Enterprise tier. Who should I talk to?", "fallback_category": "Billing", "fallback_priority": "low"},
        {"customer_name": "George Miller", "message": "Can you add support for dark mode? My eyes are hurting at night.", "fallback_category": "Feature Request", "fallback_priority": "low"},
        {"customer_name": "Hannah Abbott", "message": "I found a typo on the landing page, 'Suport' should be 'Support'.", "fallback_category": "General Inquiry", "fallback_priority": "low"},
        {"customer_name": "Ian McKellen", "message": "My payment failed but my credit card was still charged. Please check ASAP.", "fallback_category": "Billing", "fallback_priority": "high"},
        {"customer_name": "Julia Roberts", "message": "Just wanted to say that your new UI looks amazing! Great job team.", "fallback_category": "General Inquiry", "fallback_priority": "low"}
    ]

    async with AsyncSessionLocal() as session:
        for ticket_data in tickets_to_seed:
            try:
                ai_result = await ai_service.classify_ticket(ticket_data["message"])
                category = ai_result.get("category") or ticket_data["fallback_category"]
                priority = ai_result.get("priority") or ticket_data["fallback_priority"]
                # If AI returned generic fallback for all tickets, prefer preset for realistic prototype
                if category == "General Support" and ticket_data["fallback_category"] != "General Support":
                    # Keep AI only if it produced a meaningful category, otherwise use preset
                    # Heuristic: use AI if not default low-priority General Support, else preset
                    if ai_result.get("category") == "General Support" and ai_result.get("priority") == "low":
                        category = ticket_data["fallback_category"]
                        priority = ticket_data["fallback_priority"]
            except Exception as e:
                print(f"AI classification failed for {ticket_data['customer_name']}: {e}, using fallback.")
                category = ticket_data["fallback_category"]
                priority = ticket_data["fallback_priority"]

            new_ticket = Ticket(
                customer_name=ticket_data["customer_name"],
                message=ticket_data["message"],
                category=category,
                priority=priority
            )
            session.add(new_ticket)
        await session.commit()
    print("Database seeded successfully with 10 records.")
