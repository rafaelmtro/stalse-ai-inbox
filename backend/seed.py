import asyncio
from database.models import AsyncSessionLocal, Ticket, init_db
from services.ai.ollama_service import ai_service

async def seed_data():
    print("Initializing database...")
    await init_db()
    
    tickets_to_seed = [
        {"customer_name": "Alice Smith", "message": "I can't log in to my account. It says 'invalid credentials' even after a password reset."},
        {"customer_name": "Bob Johnson", "message": "I'd like to request a refund for my last invoice #12345. I was double charged."},
        {"customer_name": "Charlie Brown", "message": "The dashboard is loading very slowly today. It takes about 30 seconds to see my stats."},
        {"done_name": "Diana Prince", "message": "Is there a way to export my data to a CSV format? I couldn't find it in the settings."},
        {"customer_name": "Edward Norton", "message": "Your service is down again! This is the third time this week. I'm losing money!"},
        {"customer_name": "Fiona Gallagher", "message": "I want to upgrade my plan to the Enterprise tier. Who should I talk to?"},
        {"customer_name": "George Miller", "message": "Can you add support for dark mode? My eyes are hurting at night."},
        {"customer_name": "Hannah Abbott", "message": "I found a typo on the landing page, 'Suport' should be 'Support'."},
        {"customer_name": "Ian McKellen", "message": "My payment failed but my credit card was still charged. Please check ASAP."},
        {"customer_name": "Julia Roberts", "message": "Just wanted to say that your new UI looks amazing! Great job team."}
    ]
    
    async with AsyncSessionLocal() as session:
        print(f"Seeding {len(tickets_to_seed)} tickets with local AI classification...")
        
        for ticket_data in tickets_to_seed:
            print(f"Classifying ticket from {ticket_data.get('customer_name', 'Unknown')}...")
            ai_result = await ai_service.classify_ticket(ticket_data["message"])
            
            new_ticket = Ticket(
                customer_name=ticket_data.get("customer_name") or ticket_data.get("done_name"),
                message=ticket_data["message"],
                category=ai_result.get("category", "General Support"),
                priority=ai_result.get("priority", "low")
            )
            session.add(new_ticket)
            
        await session.commit()
        print("Database seeded successfully!")

if __name__ == "__main__":
    asyncio.run(seed_data())
