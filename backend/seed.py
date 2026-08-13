import asyncio
from pathlib import Path
from sqlalchemy import delete
from database.models import AsyncSessionLocal, Ticket, DATABASE_PATH, engine, Base
from services.ai.spark import ai_service

async def seed_data():
    print("Initializing database...")
    # Ensure parent dir exists (critical for Docker volume and local dev)
    Path(DATABASE_PATH).parent.mkdir(parents=True, exist_ok=True)

    # Create tables (idempotent)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Clear existing for deterministic prototype (10 tickets)
    async with AsyncSessionLocal() as session:
        await session.execute(delete(Ticket))
        await session.commit()
        print("Cleared existing tickets. Preparing fresh seed...")

    # Fixed typo: Diana Prince was 'done_name' previously
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
        print(f"Seeding {len(tickets_to_seed)} tickets with AI classification (fallback deterministic)...")

        for ticket_data in tickets_to_seed:
            print(f"Classifying ticket from {ticket_data['customer_name']}...")
            try:
                ai_result = await ai_service.classify_ticket(ticket_data["message"])
                category = ai_result.get("category") or ticket_data["fallback_category"]
                priority = ai_result.get("priority") or ticket_data["fallback_priority"]
                # Prefer fallback if AI only returned generic default
                if category == "General Support" and ai_result.get("category") == "General Support" and ai_result.get("priority") == "low":
                    if ticket_data["fallback_category"] != "General Support":
                        category = ticket_data["fallback_category"]
                        priority = ticket_data["fallback_priority"]
            except Exception as e:
                print(f"  AI failed ({e}), using fallback.")
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
        print("Database seeded successfully with 10 records!")

if __name__ == "__main__":
    asyncio.run(seed_data())
